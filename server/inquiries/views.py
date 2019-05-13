from django.views import generic
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datatableview.views import DatatableView
from datatableview import helpers
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
import urllib
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from core.utils import filter_queryset, send_email, get_customer_emails
from core.permissions import (
    can_view_inquiry,
)
from core.models import (
    Move, Checklist, QuoteItem, QuoteItemType,
    Customer, PropertyDetails, MoveStatus, PropertyDestinationDetails,
    Survey, Quotation, Settings, MoveTeam, TraineeTeam,
    MoveLogs, Delight)
from core.mixins import GetMoveObjMixin
from .forms import (
    NewCustomerInquiryForm, InquiryDetailsForm,
    PropertyDetailsForm)
from surveys.forms import (SurveyForm, )


class InquiryListView(DatatableView):
    template_name = 'inquiries/list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Source", 'customer__source__name'),
            ("Created Time", 'get_formatted_datetime'),
        ],
    }

    @method_decorator(user_passes_test(can_view_inquiry))
    def dispatch(self, *args, **kwargs):
        return super(InquiryListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "inquiry", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(InquiryListView, self).get_context_data(*args, **kwargs)
        context['inquiry_show'] = True
        return context


class InquiryDetailView(generic.DetailView):
    template_name = 'inquiries/detail.html'
    model = Move

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InquiryDetailView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        move_id = self.kwargs.get(self.pk_url_kwarg)
        user = self.request.user
        if user.is_superuser or user.has_perm("core.can_view_unassigned_move"):
            move = Move.objects.get(id=move_id)
        else:
            move = Move.objects.get(
                Q(move_team__moveteammember__user=user) | Q(survey__surveyor=user),
                id=move_id)
        return move

    def get_context_data(self, **kwargs):
        cxt = super(InquiryDetailView, self).get_context_data(**kwargs)
        move = self.get_object()

        payload = {
            'move': move,
            'property_form': PropertyDetailsForm(instance=move.property_details),
            'survey_form': SurveyForm(instance=move.survey)

        }
        # checklist is not available until Survey Phase
        statuses = (
            'survey', 'quotation', 'invoice', 'pre-move', 'move', 'post-move',
            'complete')
        if move.move_status.name in statuses:
            checklist = Checklist.objects.get(move=move)

            payload['checklist'] = checklist

        statuses = ('pre-move', 'move', 'post-move', 'complete')
        if move.move_status.name in statuses:
            packlist_items = checklist.checklistitem_set.filter(is_packed=True)

            required_labour = QuoteItem.objects.filter(
                Q(quotation=move.checklist.quotation) &
                Q(quote_item_type=QuoteItemType.objects.get(name="labour")))
            move_team_members = move.move_team.moveteammember_set.all()
            trainees = move.trainee_team.traineeteammember_set.all()
            move_vehicles = move.move_vehicles.all()

            payload['packlist_items'] = packlist_items
            payload['move_team_members'] = move_team_members
            payload['trainees'] = trainees
            payload['move_vehicles'] = move_vehicles
            payload['required_labour'] = required_labour

        cxt.update(payload)

        return cxt


class InquiryCreateView(generic.edit.FormView):
    template_name = 'inquiries/create-modal.html'
    form_class = NewCustomerInquiryForm
    success_url = '/inquiry/{}/property/new/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_inquiry))
    def dispatch(self, *args, **kwargs):
        return super(InquiryCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        customer_id = self.kwargs.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        # create a move record in the inquiry stage
        move = Move()
        move.customer = customer
        move.move_status = MoveStatus.objects.get(name="inquiry")
        move.move_type = form.cleaned_data['move_type']
        # generate hash using django's password maker
        hash = str(datetime.now()) + customer.user.email
        hash = make_password(password=hash, salt=None, hasher='default')
        hash = urllib.quote_plus(hash)
        move.hash = hash

        # create property and survey objects
        property_details = PropertyDetails()
        property_details.save()

        property_destination = PropertyDestinationDetails()
        property_destination.save()

        survey = Survey()
        survey.save()

        move.property_details = property_details
        move.property_destination_details = property_destination
        move.survey = survey
        # assign current user as move_rep
        move.move_rep = self.request.user
        move.save()

        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(move).pk,
            object_id=move.pk,
            object_repr=force_unicode(move),
            action_flag=ADDITION
        )

        # create checklist with empty quotation
        quote = Quotation()
        quote.profit_margin = float(
            Settings.objects.get(name='profit_margin').value)
        quote.commission = float(
            Settings.objects.get(name='commission').value)
        quote.vat = float(Settings.objects.get(name='vat').value)
        quote.save()

        checklist = Checklist()
        checklist.move = move
        checklist.quotation = quote
        checklist.save()

        # create MoveTeam, TraineeTeam, MoveVehicle, Packlist
        move.move_team = MoveTeam.objects.create()
        move.trainee_team = TraineeTeam.objects.create()
        move.delight = Delight.objects.create()

        move.save()

        # log the inquiry
        log = MoveLogs()
        log.move_status = MoveStatus.objects.get(name="inquiry")
        log.move = move
        log.move_rep = self.request.user
        log.save()

        # email the customer with a hashed callback url
        # containing move_id to finish the details
        email_ctx = {
            'full_name': customer.full_name,
            'move_id': move.id,
            'hash': hash,
            'host': self.request.get_host(),
            'subject': 'Cubemovers Move Inquiry',
            'title': 'Inquiry details',
            'recipients': get_customer_emails(customer)
        }

        send_email('inquiries/email.txt', email_ctx)

        text = "Inquiry created successfully"
        messages.add_message(self.request, messages.INFO, text)

        return redirect(self.success_url.format(move.id))


class InquiryDetailsCreateView(GetMoveObjMixin, generic.edit.FormView):
    template_name = 'inquiries/create-details.html'
    form_class = InquiryDetailsForm
    success_url = '/inquiry/{}/'
    pk_url_kwarg = 'pk'
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_inquiry))
    def dispatch(self, *args, **kwargs):
        return super(InquiryDetailsCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super(InquiryDetailsCreateView, self).get_context_data(**kwargs)
        cxt.update({'move': self.get_object()})
        return cxt

    def form_valid(self, form):
        move = self.get_object()
        property_details = move.property_details
        property_details.primary_area_name = form.cleaned_data['primary_area_name']
        property_details.secondary_area_name = form.cleaned_data['secondary_area_name']
        property_details.street_name = form.cleaned_data['street_name']
        property_details.secondary_street_name = form.cleaned_data['secondary_street_name']
        property_details.gate_color = form.cleaned_data['gate_color']
        property_details.compound_name = form.cleaned_data['compound_name']
        property_details.house_no = form.cleaned_data['house_no']
        property_details.floor = form.cleaned_data['floor']
        property_details.land_marks = form.cleaned_data['land_marks']
        property_details.side_of_road = form.cleaned_data['side_of_road']
        property_details.save()

        survey = move.survey
        survey.survey_time = form.cleaned_data['survey_time']
        survey.move_time = form.cleaned_data['move_time']
        survey.save()

        # update Move status to pre-survey
        move.move_status = MoveStatus.objects.get(name='pre-survey')
        # TODO: automatically add a surveyor
        move.save()

        log = MoveLogs()
        log.move_status = MoveStatus.objects.get(name="pre-survey")
        log.move = move
        log.move_rep = self.request.user
        log.save()

        text = "Property details saved"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(self.get_object().id))


class CustomerUpdateView(generic.UpdateView):
    model = PropertyDetails
    form_class = PropertyDetailsForm
    template_name = 'inquiries/property_modal.html'
    success_url = '/inquiry/{}/'
    obj = None
    move = None

    def get_object(self, queryset=None):
        return self.get_move().move.property_details

    def get_move(self):
        if not self.obj:
            id = self.kwargs.get(self.pk_url_kwarg)
            self.obj = PropertyDetails.objects.get(id=id)
        return self.obj

    def get_success_url(self):
        return self.success_url.format(self.get_move().id)
