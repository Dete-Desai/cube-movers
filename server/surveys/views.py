from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from django.utils.timezone import localtime
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from core.permissions import (
    can_view_inquiry, can_view_surveys, can_view_pre_survey
)
from core.utils import send_sms, send_email
from core.mixins import GetMoveObjMixin
from core.models import (
    MoveLogs, MoveStatus, Checklist, ChecklistItem, Room, Item,
    Move, Office)
from datatableview.views import DatatableView
from datatableview import helpers
from inquiries.forms import (PropertyDetailsForm, )
from core.utils import filter_queryset, recompute_checklist_totals
from core.mixins import GetChecklistObjMixin
from .forms import (
    SurveyForm, ChecklistAddNewForm, ChecklistDeleteForm,
    ChecklistEditForm, SurveyInstructionsForm)


class CreateSurveyView(GetMoveObjMixin, generic.edit.FormView):
    template_name = 'surveys/edit-modal.html'
    form_class = SurveyForm
    success_url = '/inquiry/{}/'
    obj = None
    pk_url_kwarg = 'pk'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_inquiry))
    def dispatch(self, *args, **kwargs):
        return super(CreateSurveyView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super(CreateSurveyView, self).get_context_data(**kwargs)
        cxt.update({'move': self.get_object()})
        return cxt

    def form_valid(self, form):
        survey = form.save()
        move = self.get_object()
        move.survey = survey
        move.save()
        if 'survey_time' in form.cleaned_data and form.cleaned_data['survey_time']:
            survey.survey_time = form.cleaned_data['survey_time']
            survey.save()

        if hasattr(survey.surveyor, 'staffprofile') and survey.surveyor.staffprofile.phone_number:
            host_name = self.request.get_host()
            full_name = survey.surveyor.get_full_name()
            phone_number = survey.surveyor.staffprofile.phone_number
            message = (
                "Hello %s. You have been assigned a survery. Login to  "
                "https://%s for more details" %
                (str(full_name), str(host_name)))
            send_sms(phone_number, message)

        text = "Survey updated successfully"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(self.get_object().id))

    def get_success_url(self):
        return self.success_url.format(self.get_object().id)

    def form_invalid(self, form):
        self.get_context_data(form=form)
        return redirect(self.get_success_url())


class ConfirmSurveyView(GetMoveObjMixin, generic.View):
    template_name = 'surveys/confirm-modal.html'
    success_url = '/inquiry/{}/'
    obj = None
    pk_url_kwarg = 'pk'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_inquiry))
    def dispatch(self, *args, **kwargs):
        return super(ConfirmSurveyView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        move = self.get_object()
        if not request.POST.get('skip', False):
            customer = move.customer
            email_ctx = {
                'full_name': customer.full_name,
                'move_id': move.id,
                'hash': hash,
                'host': self.request.get_host(),
                'subject': 'Cubemovers Survey Confirmation',
                'title': 'Confirmation of Pre-Move Survey Appointment',
                'recipients': [customer.user.email],
                'survey_time': move.survey.survey_time,
                'surveyor': move.survey.surveyor,
                'survey': move.survey
            }
            # send customer email

            send_email('surveys/emails/customer.txt', email_ctx)

            # send surveyor email
            email_ctx['full_name'] = move.survey.surveyor.first_name
            email_ctx['recipients'] = [move.survey.surveyor.email]
            send_email('surveys/emails/surveyor.txt', email_ctx)

            # send sms to customer
            to = customer.phone_number
            local_time = localtime(move.survey.survey_time)
            message = "Dear %s, We are happy to confirm that your survey appointment has been scheduled for %s with %s %s" % (customer.full_name, local_time.strftime("%d/%m/%Y %-I:%M %p"), move.survey.surveyor.first_name, move.survey.surveyor.last_name)
            send_sms(to, message)

        # update Move to next phase
        move.move_status = MoveStatus.objects.get(name="survey")
        move.save()

        # log but check if there is a previous entry
        if not MoveLogs.objects.filter(
            Q(move=move) & Q(move_status=MoveStatus.objects.get(name="survey"))
        ).exists():
            log = MoveLogs()
            log.move_status = MoveStatus.objects.get(name="survey")
            log.move = move
            log.move_rep = request.user
            log.save()

        text = "Checklist ready for survey"
        messages.add_message(request, messages.INFO, text)

        text = "Pre-survey complete. You can now conduct the actual Survey"
        messages.add_message(request, messages.INFO, text)
        return redirect(self.success_url.format(self.get_object().id))


class SurveyChecklistView(generic.DetailView):
    model = Checklist
    template_name = 'surveys/checklist.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SurveyChecklistView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super(SurveyChecklistView, self).get_context_data(**kwargs)
        checklist = self.get_object()
        checklist_items = ChecklistItem.objects.filter(checklist=checklist)
        items = Item.objects.all()
        move_type = checklist.move.move_type.name
        offices = []
        # return rooms based on the move_type
        if move_type == "House Move":
            rooms = Room.objects.filter(room_type="house")
        elif move_type == "Office Move":
            rooms = Room.objects.filter(room_type="office")
            offices = Office.objects.all()
        elif move_type == "Storage and Warehousing":
            rooms = Room.objects.all()

        payload = {
            'checklist': checklist,
            'checklist_items': checklist_items,
            'rooms': rooms,
            'items': items,
            'move_type': move_type,
            'offices': offices
        }
        cxt.update(payload)
        return cxt


class CreateSurveyDestinationView(GetMoveObjMixin, generic.edit.FormView):
    template_name = 'surveys/destination.html'
    form_class = PropertyDetailsForm
    success_url = '/surveys/{}/destination/'
    obj = None
    pk_url_kwarg = 'pk'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_surveys))
    def dispatch(self, *args, **kwargs):
        return super(CreateSurveyDestinationView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super(CreateSurveyDestinationView, self).get_context_data(**kwargs)
        cxt.update({'move': self.get_object()})
        return cxt

    def form_valid(self, form):
        move = self.get_object()
        property_details = move.property_destination_details
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

        text = "Destination property details saved"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(self.get_object().id))


class PresurveyListView(DatatableView):
    model = Move
    template_name = 'surveys/presurvey_list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Created Time", 'get_formatted_datetime'),
        ],
    }

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_survey))
    def dispatch(self, *args, **kwargs):
        return super(PresurveyListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "pre-survey", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(PresurveyListView, self).get_context_data(*args, **kwargs)
        context['presurvey_show'] = True
        return context


class SurveyListView(DatatableView):
    model = Move
    template_name = 'surveys/survey_list.html'

    @helpers.keyed_helper
    def get_surveyor_name(instance, text=None, *args, **kwargs):
        return instance.survey.surveyor.get_full_name()

    @helpers.keyed_helper
    def get_survey_move_time(instance, text=None, *args, **kwargs):
        return instance.survey.get_formatted_survey_date()

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ('Move Rep', 'survey__surveyor__first_name', get_surveyor_name),
            ("Survey Date", 'survey__move_time', get_survey_move_time),
            ('Car Allocated', 'survey__vehicle__registration'),
        ],
        'ordering': ['-survey__survey_time']
    }

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_surveys))
    def dispatch(self, *args, **kwargs):
        return super(SurveyListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "survey", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(SurveyListView, self).get_context_data(*args, **kwargs)
        context['survey_show'] = True
        return context


class SurveyChecklistAddExistingItemView(GetChecklistObjMixin, generic.View):
    success_url = '/surveys/checklist/{}/'
    pk_url_kwarg = 'checklist_id'
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_surveys))
    def dispatch(self, *args, **kwargs):
        return super(SurveyChecklistAddExistingItemView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('room_id'):
            checklist = self.get_object()
            room = Room.objects.get(id=request.POST.get('room_id'))
            # make office null on house move
            move_type = checklist.move.move_type.name

            for item in request.POST:
                if 'item' in item:
                    value = request.POST.get(item)
                    if int(value) and int(value) > 0:
                        item_array = item.split('_')
                        item_id = int(item_array[1])
                        item = Item.objects.get(id=item_id)

                        try:
                            if move_type == "Office Move":
                                office_id = request.POST.get('office')
                                try:
                                    office = Office.objects.get(pk=office_id)
                                except Office.DoesNotExist:
                                    text = "You must first create an office before you add items"
                                    messages.add_message(request, messages.INFO, text)
                                    return redirect(self.success_url.format(checklist.id))
                                checklist_item = ChecklistItem.objects.get(
                                    room=room.id, item=item_id,
                                    checklist=checklist, office=office)
                            else:
                                checklist_item = ChecklistItem.objects.get(
                                    room=room.id, item=item_id,
                                    checklist=checklist)
                            checklist_item.qty = value

                        except ChecklistItem.DoesNotExist:
                            checklist_item = ChecklistItem()
                            checklist_item.checklist = checklist
                            checklist_item.room = room
                            checklist_item.item = item
                            checklist_item.vol = item.vol
                            checklist_item.qty = value

                        if move_type == "Office Move":
                            checklist_item.office = office
                        checklist_item.save()

                        # recompute total volume
                        items = ChecklistItem.objects.filter(
                            checklist=checklist)
                        total = 0.0
                        for item in items:
                            total += (item.vol * item.qty)

                        checklist.total_vol = total
                        checklist.save()
            text = "Items Added"
            messages.add_message(request, messages.INFO, text)
            return redirect(self.success_url.format(checklist.id))
        else:
            text = "There was an error adding the item"
            messages.add_message(request, messages.ERROR, text)
            return redirect(self.success_url.format(checklist.id))


class SurveyChecklistAddNewItemView(GetChecklistObjMixin, generic.edit.FormView):
    success_url = '/surveys/checklist/{}/'
    form_class = ChecklistAddNewForm
    pk_url_kwarg = 'checklist_id'
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_surveys))
    def dispatch(self, *args, **kwargs):
        return super(SurveyChecklistAddNewItemView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        checklist = self.get_object()
        room = Room.objects.get(id=form.cleaned_data['room_id'])
        move_type = checklist.move.move_type.name

        checklist_item = ChecklistItem()
        checklist_item.checklist = checklist
        checklist_item.room = room
        checklist_item.item_backup = form.cleaned_data['name']
        checklist_item.vol = form.cleaned_data['vol']
        checklist_item.qty = form.cleaned_data['qty']
        if move_type == "Office Move":
            office_id = form.cleaned_data['office']
            office = Office.objects.get(pk=office_id)
            checklist_item.office = office
        checklist_item.save()

        # recompute total volume
        recompute_checklist_totals(checklist)

        text = "Checklist Item Added"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(checklist.id))

    def form_invalid(self, form):
        text = "There was an error adding the item"
        messages.add_message(self.request, messages.ERROR, text)
        return redirect(self.success_url.format(self.obj.id))


class SurveyChecklistItemDeleteView(GetChecklistObjMixin, generic.edit.FormView):
    model = ChecklistItem
    pk_url_kwarg = 'checklist_id'
    success_url = '/surveys/checklist/{}/'
    form_class = ChecklistDeleteForm
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_surveys))
    def dispatch(self, *args, **kwargs):
        return super(SurveyChecklistItemDeleteView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        checklist = self.get_object()
        item = ChecklistItem.objects.get(id=form.cleaned_data['item_id'])
        item.delete()
        recompute_checklist_totals(checklist)
        text = "Checklist Item Deleted"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(self.obj.id))


class SurveyChecklistItemEditView(GetChecklistObjMixin, generic.edit.FormView):
    model = ChecklistItem
    pk_url_kwarg = 'checklist_id'
    success_url = '/surveys/checklist/{}/'
    form_class = ChecklistEditForm
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_surveys))
    def dispatch(self, *args, **kwargs):
        return super(SurveyChecklistItemEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        item = ChecklistItem.objects.get(id=form.cleaned_data['item_id'])
        item.vol = form.cleaned_data['vol']
        item.qty = form.cleaned_data['qty']
        item.save()

        recompute_checklist_totals(item.checklist)

        text = "Checklist Item Edited"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(self.get_object().id))


class SurveyInstructionsView(GetChecklistObjMixin, generic.edit.FormView):
    model = ChecklistItem
    pk_url_kwarg = 'checklist_id'
    success_url = '/surveys/checklist/{}/'
    form_class = SurveyInstructionsForm
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_surveys))
    def dispatch(self, *args, **kwargs):
        return super(SurveyInstructionsView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        checklist = self.get_object()
        move = Move.objects.get(checklist=checklist.id)
        move.special_instructions = form.cleaned_data['special_instructions']
        move.accessibility_instructions = form.cleaned_data['access_instructions']
        move.save()
        text = "Instructions updated successfully"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(self.get_object().id))
