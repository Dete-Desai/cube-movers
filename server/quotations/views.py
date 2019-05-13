import random
from datetime import datetime
import string
import os
import urllib
import uuid
from django.contrib import messages
from django.conf import settings
from easy_pdf import rendering
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.views import generic
from django.utils.encoding import force_unicode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from datatableview.views import DatatableView
from easy_pdf.views import PDFTemplateView
from datatableview import helpers
from core.permissions import (
    can_view_quotes,
)
from core.models import (
    Quotation, QuoteItem, QuoteItemDefault, ChecklistItem,
    MoveStatus, MoveLogs, Move, QuoteDocument)
from core.tasks import send_email as send_quotation_email
from core.utils import (
    send_sms, recompute_quote_totals, get_customer_emails,
    generate_quotation_number)
from .forms import (
    QuoteApprovalForm, QuoteRejectForm, QuoteDateForm,
    QuoteItemEditForm, QuoteItemDeleteForm, QuoteParametersForm,
    EditQuoteForm)
from .mixins import QuotationDetailViewMixin


def get_move_tpl(move_type):
    move_typ = move_type.upper().replace(' ', '_').strip()
    return settings.MOVE_PDF_TPLS.get(move_typ, settings.MOVE_PDF_TPLS['DEFAULT'])


class QuotationDetailView(QuotationDetailViewMixin, generic.DetailView):
    model = Quotation
    template_name = 'quotations/quotations.html'


class AddQuotationMoveDateView(QuotationDetailViewMixin, generic.edit.FormView):
    success_url = '/quotations/{}/'
    model = Quotation
    form_class = QuoteDateForm
    template_name = 'quotations/quotations.html'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        quote = self.get_object()
        move = Move.objects.get(id=form.cleaned_data['move_id'])
        move.move_date = form.cleaned_data['date']
        move.save()

        text = "Date Set"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(quote.id))


class SendQuotationView(generic.View):
    model = Quotation
    template_name = 'quotations/send-modal.html'
    success_url = '/inquiry/{}/'
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        quotation_id = kwargs.get(self.pk_url_kwarg)
        quote = self.model.objects.get(pk=quotation_id)
        move = quote.checklist.move
        # generate token
        token = ''.join(
            random.choice(
                string.ascii_uppercase + string.digits) for _ in range(5))
        move.token = token
        quoted_hash = uuid.uuid4()
        quote.hash = quoted_hash
        quote.status = "sent"
        quote.sent_time = datetime.now()
        quote.save()

        context = {
            'move': move,
            'quote': quote,
            'datetime': datetime.now(),
            'quote_items': QuoteItem.objects.filter(quotation=quote),
            'hash': quoted_hash,
            'host': self.request.get_host()
        }
        payload = {
            'inventory': ChecklistItem.objects.filter(checklist=move.checklist)
        }
        quote_inventory_temp = rendering.render_to_pdf(
            'quotations/pdf/quote_inventory.html', payload
        )

        quote_temp = rendering.render_to_pdf(
            get_move_tpl(move.move_type.name),
            {'move': move}
        )
        if not quote.quote_number:
            quote.quote_number = generate_quotation_number(move)
            quote.save()
        subject_quote = (
            "[ # " + quote.quote_number + "]: " + "Cubemovers Quotation"
        )

        data = {
            'plaintext': 'quotations/emails/quote_email.txt',
            'html': 'quotations/emails/quote_email.html',
            'context': context,
            'subject': subject_quote,
            'from': settings.EMAIL_HOST_USER,
            'to': get_customer_emails(move.customer),
            'local_quote': quote_temp,
            'inventory': quote_inventory_temp,
            'cc': settings.QUOTATION_EMAILS_CC
        }

        send_quotation_email.delay(**data)

        # shift Move Record to the Quotation phase
        move.move_status = MoveStatus.objects.get(name="quotation")
        move.save()

        # log but check if there is a previous entry
        if not MoveLogs.objects.filter(
            Q(move=move) & Q(move_status=MoveStatus.objects.get(
                name="quotation"))).exists():
            log = MoveLogs()
            log.move_status = MoveStatus.objects.get(name="quotation")
            log.move = move
            log.move_rep = self.request.user
            log.save()

        text = "Survey complete. Quotation awaiting approval"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(move.id))


class QuotationApprovalView(generic.View):
    model = Quotation
    form_class = QuoteApprovalForm
    template_name = 'quotations/send-modal.html'
    success_url = '/inquiry/{}/'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        form = QuoteApprovalForm(request.GET)
        if form.is_valid():
            try:
                Quotation.objects.get(
                    id=form.cleaned_data['quote_id'],
                    hash=form.cleaned_data['hash'])
            except Quotation.DoesNotExist:
                return render(request, 'quotations/approval-error.html')

            quote = get_object_or_404(Quotation, pk=form.cleaned_data['quote_id'])
            move = quote.checklist.move
            # change Quote status
            quote.status = "approved"
            quote.reply_time = datetime.now()
            quote.save()

            payload = {
                'move': move
            }
            # email quality guys and cc the move_rep
            context = {
                'move': move,
                'quote': quote,
                'datetime': datetime.now(),
                'host': request.get_host()
            }
            data = {
                'plaintext': 'quotations/emails/quote_accept_email.txt',
                'html': 'quotations/emails/quote_accept_email.html',
                'context': context,
                'subject': 'Quotation Accepted',
                'from': settings.EMAIL_HOST_USER,
                'to': settings.CUBEMOVERS['quality_email'],
                'cc': move.survey.surveyor.email
            }

            # send customer important notice.

            data_customer = {
                'plaintext': 'customers/emails/important_notice_email.txt',
                'html': 'customers/emails/important_notice_email.html',
                'subject': 'Important Advice',
                'from': settings.EMAIL_HOST_USER,
                'to': get_customer_emails(move.customer),
                'context': context,
                'important_notice': True
            }
            to = move.customer.phone_number
            message = ("Dear %s, Thank you for accepting to move with us."
                       "Your secret token is %s. Keep the token safe you will "
                       "require it at the end of the move." %
                       (move.customer.full_name, move.token))
            send_sms(to, message)

            send_quotation_email.delay(**data)
            send_quotation_email.delay(**data_customer)

            return render(request, 'quotations/quote_approved.html', payload)


class QuotationRejectionView(generic.View):
    model = Quotation

    def get(self, request, *args, **kwargs):
        form = QuoteApprovalForm(request.GET)
        if form.is_valid():
            # cross-check url hash
            if not Quotation.objects.filter(
                Q(id=form.cleaned_data['quote_id']) & Q(hash=urllib.quote_plus(form.cleaned_data['hash']))
            ).exists():
                return render(request, 'quotations/approval-error.html')

            quote = get_object_or_404(Quotation, pk=form.cleaned_data['quote_id'])
            move = quote.checklist.move

            # change Quote status

            quote.status = "rejected"
            quote.reply_time = datetime.now()
            quote.save()

            # email quality guys and cc move reps
            context = {
                'move': move,
                'quote': quote,
                'datetime': datetime.now(),
                'host': request.get_host()
            }

            data = {
                'plaintext': 'quotations/emails/quote_reject_email.txt',
                'html': 'quotations/emails/quote_reject_email.html',
                'context': context,
                'subject': 'Quotation Rejected',
                'from': settings.EMAIL_HOST_USER,
                'to': settings.CUBEMOVERS['quality_email'],
                'cc': move.survey.surveyor.email
            }

            send_quotation_email.delay(**data)

            payload = {
                'move': move
            }
            return render(request, 'quotations/quote_rejected.html', payload)

    def post(self, request, *args, **kwargs):
        form = QuoteRejectForm(request.POST)

        if form.is_valid():
            move = Move.objects.get(id=form.cleaned_data['move_id'])
            quotation = move.checklist.quotation
            quotation.reject_reason = form.cleaned_data['reason']
            quotation.save()

            text = "Submitted Successfully"
            messages.add_message(request, messages.INFO, text)
            return render(request, 'quotations/quote_rejected_sent.html')


class QuotationsListView(DatatableView):
    model = Move
    template_name = 'quotations/quotations_list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Survey Date", 'survey__get_formatted_survey_date'),
            ("Proposed Move Date", 'get_formatted_move_date'),
            ("Created Time", 'get_formatted_datetime')
        ],
        'ordering': ['survey__survey_time']
    }

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(QuotationsListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("core.can_view_unassigned_move"):
            return Move.objects.filter(
                ~Q(checklist__quotation__status="rejected"),
                move_status=MoveStatus.objects.get(name='quotation'))
        else:
            return Move.objects.filter(
                ~Q(checklist__quotation__status="rejected"),
                move_status=MoveStatus.objects.get(name='quotation'),
                survey__surveyor=user)

    def get_context_data(self, *args, **kwargs):
        context = super(QuotationsListView, self).get_context_data(*args, **kwargs)
        context['quote_show'] = True
        return context


class RejectedQuotationsListView(DatatableView):
    model = Move
    template_name = 'quotations/rejected_quote_list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Survey Time", 'survey__get_formatted_survey_date'),
            ("Proposed Move Time", 'get_formatted_move_date'),
            ("Created Time", 'get_formatted_datetime')
        ],
        'ordering': ['survey__survey_time']
    }

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(RejectedQuotationsListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("core.can_view_unassigned_move"):
            return Move.objects.filter(
                checklist__quotation__status="rejected",
                move_status=MoveStatus.objects.get(name='quotation'))
        else:
            return Move.objects.filter(
                checklist__quotation__status="rejected",
                move_status=MoveStatus.objects.get(name='quotation'),
                survey__surveyor=user)

    def get_context_data(self, *args, **kwargs):
        context = super(
            RejectedQuotationsListView, self).get_context_data(*args, **kwargs)
        context['rejected_quote_show'] = True
        return context


class AddSurveyQuotationView(generic.View):
    model = Quotation
    success_url = '/quotations/{}/'
    pk_url_kwarg = 'pk'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(AddSurveyQuotationView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        quotation_id = kwargs.get(self.pk_url_kwarg)
        quote = Quotation.objects.get(id=quotation_id)
        for item in request.POST:
            if 'item' in item:
                value = request.POST.get(item)
                if int(value) and int(value) > 0:
                    quote_item_array = item.split('_')
                    quote_item_id = int(quote_item_array[1])
                    # retrieve Defaults for reference
                    quoteItemDefault = QuoteItemDefault.objects.get(
                        id=quote_item_id)

                    # generate new Item for quotation
                    try:
                        quoteItem = QuoteItem.objects.get(
                            quotation=quote,
                            quote_item_type=quoteItemDefault.quote_item_type,
                            item=quoteItemDefault.item)
                        quoteItem.units = value
                    except QuoteItem.DoesNotExist:
                        quoteItem = QuoteItem()
                        quoteItem.quotation = quote
                        quoteItem.item = quoteItemDefault.item
                        quoteItem.cost = quoteItemDefault.cost
                        quoteItem.units = value
                        quoteItem.quote_item_type = \
                            quoteItemDefault.quote_item_type
                    quoteItem.save()

                    # Add a log entries
                    quote.move_rep = request.user
                    quote.save()

                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(
                            quote).pk,
                        object_id=quote.pk,
                        object_repr=force_unicode(quote),
                        action_flag=CHANGE
                    )

                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(
                            quoteItem).pk,
                        object_id=quoteItem.pk,
                        object_repr=force_unicode(quoteItem),
                        action_flag=ADDITION
                    )
                    # recompute totals
        recompute_quote_totals(quote)
        text = "Quote Item Added"
        messages.add_message(request, messages.INFO, text)
        return redirect(self.success_url.format(quote.id))


class EditSurveyQuotationsItemView(generic.edit.FormView):
    success_url = '/quotations/{}/'
    form_class = QuoteItemEditForm
    pk_url_kwarg = 'pk'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(EditSurveyQuotationsItemView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        quotation_id = self.kwargs.get(self.pk_url_kwarg)
        quote = Quotation.objects.get(id=quotation_id)
        item = QuoteItem.objects.get(id=form.cleaned_data['quote_id'])
        item.units = form.cleaned_data['units']
        item.cost = form.cleaned_data['cost']
        item.save()

        recompute_quote_totals(item.quotation)

        text = "Quote Item Modified"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(quote.id))


class DeleteSurveyQuotationsItemView(generic.edit.FormView):
    success_url = '/quotations/{}/'
    form_class = QuoteItemDeleteForm
    pk_url_kwarg = 'pk'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(DeleteSurveyQuotationsItemView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        quotation_id = self.kwargs.get(self.pk_url_kwarg)
        quote = Quotation.objects.get(id=quotation_id)
        item = QuoteItem.objects.get(id=form.cleaned_data['quote_id'])
        item.delete()

        recompute_quote_totals(item.quotation)

        text = "Quote Item Deleted"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(quote.id))


class AddQuotationsParametersView(generic.edit.FormView):
    success_url = '/quotations/{}/'
    form_class = QuoteParametersForm
    pk_url_kwarg = 'pk'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(AddQuotationsParametersView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        quotation_id = self.kwargs.get(self.pk_url_kwarg)
        quote = Quotation.objects.get(id=quotation_id)
        quote.profit_margin = form.cleaned_data['profit_margin']
        quote.commission = form.cleaned_data['commission']
        quote.vat = form.cleaned_data['vat']
        quote.discount = form.cleaned_data['discount']
        quote.save()
        recompute_quote_totals(quote)
        text = "Quote Parameters Modified"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(quote.id))


class EditQuotationsView(generic.edit.FormView):
    form_class = EditQuoteForm
    success_url = '/inquiry/{}/'
    template_name = 'quotations/quotations-edit.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(EditQuotationsView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            a = QuoteDocument.objects.get(move=form.cleaned_data['move'])
            a.quote_content = form.cleaned_data['quote_content']
            a.save()
        except QuoteDocument.DoesNotExist:
            move = Move.objects.get(pk=form.cleaned_data['move'])
            QuoteDocument.objects.create(
                move=move,
                quote_content=form.cleaned_data['quote_content'])

        return redirect(self.success_url.format(self.kwargs['move_id']))

    def get_initial(self):
        move = Move.objects.get(id=self.kwargs['move_id'])
        try:
            q = QuoteDocument.objects.get(move=self.kwargs['move_id'])
            quote_content = q.quote_content
        except QuoteDocument.DoesNotExist:
            b_path = 'moves/templates/moves/documents/'
            filename = os.path.join(b_path, 'house_base.txt')
            if move.move_type.name == "Office Move":
                filename = os.path.join(b_path, 'office_base.txt')
            elif move.move_type.name == "Storage and Warehousing":
                filename = os.path.join(b_path, 'storage_base.txt')
            with open(filename, 'r') as quote_file:
                quote_content = quote_file.read()

        self.initial.update({'move': self.kwargs['move_id']})
        self.initial.update({'quote_content': quote_content})
        return super(EditQuotationsView, self).get_initial()

    def get_context_data(self, *args, **kwargs):

        context = super(EditQuotationsView, self).get_context_data(*args, **kwargs)
        context['move'] = get_object_or_404(Move, pk=self.kwargs['move_id'])
        return context


class LocalQuotePdfView(PDFTemplateView):

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(LocalQuotePdfView, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        move = get_object_or_404(Move, pk=self.kwargs['move_id'])
        if not move.checklist.quotation.quote_number:
            move.checklist.quotation.quote_number = generate_quotation_number(move)
            move.checklist.quotation.save()
        template_office = 'moves/pdf/office.html'
        template_house_move = 'moves/pdf/default.html'
        template_storage = 'moves/pdf/storage.html'
        template_list = []
        if move.move_type.name == "Office Move":
            template_list.append(template_office)
        elif move.move_type.name == "Storage and Warehousing":
            template_list.append(template_storage)
        else:
            template_list.append(template_house_move)
        return template_list

    def get_context_data(self, *args, **kwargs):

        context = super(
            LocalQuotePdfView, self).get_context_data(*args, **kwargs)

        context['move'] = get_object_or_404(Move, pk=self.kwargs['move_id'])
        return context
