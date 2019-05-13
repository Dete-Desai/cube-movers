from django.views import generic
from django.db.models import Q
from django.shortcuts import redirect
from easy_pdf import rendering
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.shortcuts import render
from datatableview.views import DatatableView
from datatableview import helpers
from core.models import (
    Move, QuoteItem, QuoteItemType, MoveLogs, MoveStatus,
    MoveTeamMember, TraineeTeamMember, Vehicle, ChecklistItem,
    Checklist)
from core.permissions import (
    can_view_pre_move, can_view_move,
    can_view_post_move, can_view_complete_move, is_superuser
)
from core.tasks import send_email
from core.mixins import GetMoveObjMixin
from core.utils import filter_queryset
from .forms import (
    MoveUsersForm, MoveVehicleForm, MoveDetailsForm, DelightForm,
    MoveTeamLeadForm)


class MoveTeamView(generic.View):

    success_url = '/moves/{}/team/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(MoveTeamView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        form = MoveUsersForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=form.cleaned_data['user_id'])

            if MoveTeamMember.objects.filter(Q(user=user) & Q(move_team=move.move_team)).exists():
                text = "Team member already added"
                messages.add_message(request, messages.ERROR, text)
                return redirect(self.success_url.format(move.id))

            user = User.objects.get(id=form.cleaned_data['user_id'])
            move_team = move.move_team

            move_team_member = MoveTeamMember()
            move_team_member.move_team = move_team
            move_team_member.user = user
            move_team_member.save()

            text = "Move Team member added"
            messages.add_message(request, messages.INFO, text)
            return redirect(self.success_url.format(move.id))

    def get(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        movers = User.objects.filter(
            groups__name__in=['move_supervisor', 'movers'])

        team_members = move.move_team.moveteammember_set.all()
        required_labour = QuoteItem.objects.filter(
            Q(quotation=move.checklist.quotation) & Q(quote_item_type=QuoteItemType.objects.get(name="labour")))

        payload = {
            'move': move,
            'movers': movers,
            'team_members': team_members,
            'required_labour': required_labour
        }
        return render(request, 'moves/move_team.html', payload)


class MoveTeamLeadView(generic.edit.FormView):

    success_url = '/moves/{}/team/'
    form_class = MoveTeamLeadForm

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(MoveTeamLeadView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        move_id = self.kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        member = MoveTeamMember.objects.get(
            id=form.cleaned_data['member_id'])
        # remove the previous team lead
        move_team = member.move_team
        members = move_team.moveteammember_set.all()
        for mem in members:
            mem.is_lead = False
            mem.save()

        # set new lead
        member.is_lead = True
        member.save()

        text = "Team Lead set"
        messages.add_message(self.request, messages.INFO, text)
        return redirect(self.success_url.format(move.id))


class DeleteMoveTeamMemberView(generic.DeleteView):
    model = MoveTeamMember
    pk_url_kwarg = 'member_id'
    move = None

    def get_object(self, queryset=None):
        obj = super(DeleteMoveTeamMemberView, self).get_object(queryset)
        self.move = Move.objects.get(id=self.kwargs.get('move_id'))
        return obj

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Team Member removed')
        return '/moves/{}/team/'.format(self.move.id)

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(DeleteMoveTeamMemberView, self).dispatch(*args, **kwargs)


class MoveTraineesView(generic.View):

    success_url = '/moves/{}/trainees/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(MoveTraineesView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        form = MoveUsersForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=form.cleaned_data['user_id'])
            if TraineeTeamMember.objects.filter(Q(user=user) & Q(trainee_team=move.trainee_team)).exists():
                text = "Trainee already added"
                messages.add_message(request, messages.ERROR, text)
                return redirect(self.success_url.format(move.id))

            trainee_team = move.trainee_team

            member = TraineeTeamMember()
            member.trainee_team = trainee_team
            member.user = user
            member.save()

            text = "Trainee added"
            messages.add_message(request, messages.INFO, text)
            return redirect(self.success_url.format(move.id))

    def get(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        g = Group.objects.get(name='trainee')
        trainees = g.user_set.all()

        team_members = move.trainee_team.traineeteammember_set.all()

        payload = {
            'move': move,
            'trainees': trainees,
            'team_members': team_members
        }
        return render(request, 'moves/move_trainees.html', payload)


class DeleteMoveTraineesView(generic.DeleteView):
    model = TraineeTeamMember
    pk_url_kwarg = 'member_id'
    move = None

    def get_object(self, queryset=None):
        obj = super(DeleteMoveTraineesView, self).get_object(queryset)
        self.move = Move.objects.get(id=self.kwargs.get('move_id'))
        return obj

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Trainee removed')
        return '/moves/{}/trainees/'.format(self.move.id)

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(DeleteMoveTraineesView, self).dispatch(*args, **kwargs)


class MoveVehiclesView(generic.View):

    success_url = '/moves/{}/vehicles/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(MoveVehiclesView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        form = MoveVehicleForm(request.POST)
        if form.is_valid():
            move.move_vehicles.add(Vehicle.objects.get(
                id=form.cleaned_data['vehicle_id']))
            move.save()

            text = "Vehicle added"
            messages.add_message(request, messages.INFO, text)
            messages.add_message(request, messages.INFO, text)
            return redirect(self.success_url.format(move.id))

    def get(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        vehicles = Vehicle.objects.all()
        move_vehicles = move.move_vehicles.all()

        payload = {
            'move': move,
            'vehicles': vehicles,
            'move_vehicles': move_vehicles
        }
        return render(request, 'moves/move_vehicle.html', payload)


class DeleteMoveVehiclesView(generic.DeleteView):
    model = Vehicle
    pk_url_kwarg = 'vehicle_id'
    move = None

    def get_object(self, queryset=None):
        obj = super(DeleteMoveVehiclesView, self).get_object(queryset)
        self.move = Move.objects.get(id=self.kwargs.get('move_id'))
        return obj

    def delete(self, request, *args, **kwargs):
        # delink the vehicle from the move
        vehicle = self.get_object()
        self.move.move_vehicles.remove(vehicle)
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Vehicle removed')
        return '/moves/{}/vehicles/'.format(self.move.id)

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(DeleteMoveVehiclesView, self).dispatch(*args, **kwargs)


class PremoveReport(generic.View):

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(PremoveReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        report_type = kwargs.get('report_type')
        move = Move.objects.get(id=move_id)
        payload = {
            'move': move,
        }
        return rendering.render_to_pdf_response(
            request, 'moves/pre-move/{}_report_pdf.html'.format(report_type),
            payload, filename='Premove_{}_Report{}.pdf'.format(report_type, move.id))


class ConfirmMoveView(GetMoveObjMixin, generic.View):
    template_name = 'moves/pre-move/confirm-move-modal.html'
    success_url = '/inquiry/{}/'
    pk_url_kwarg = 'move_id'
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_move))
    def dispatch(self, *args, **kwargs):
        return super(ConfirmMoveView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        move = self.get_object()
        state = self.kwargs.get('state').replace('_', '-')
        move.move_status = MoveStatus.objects.get(name=state)
        move.save()
        # log but check if there is a previous entry
        if MoveLogs.objects.filter(Q(move=move) & Q(
                move_status=MoveStatus.objects.get(
                    name=state))).exists():
            pass
        else:
            log = MoveLogs()
            log.move_status = MoveStatus.objects.get(name=state)
            log.move = move
            log.move_rep = request.user
            log.save()

        msg_maps = {
            'pre-move': 'Move done. Awaiting delight form completion',
            'move': 'Move approved'
        }
        messages.add_message(request, messages.INFO, msg_maps.get(state, "Action was successful"))
        return redirect(self.success_url.format(move.id))


class CancelMoveView(GetMoveObjMixin, generic.View):
    pk_url_kwarg = 'move_id'
    obj = None
    success_url = '/moves/cancelled/list/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CancelMoveView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        move = self.get_object()
        cancelled_status = MoveStatus.objects.get(name='cancelled')
        move.move_status = cancelled_status
        move.save()
        return redirect(self.success_url)


class MovePacklistView(GetMoveObjMixin, generic.View):
    success_url = '/moves/{}/packlist/'
    pk_url_kwarg = 'move_id'
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_move))
    def dispatch(self, *args, **kwargs):
        return super(MovePacklistView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        checklist_id = kwargs.get('checklist_id')
        checklist = Checklist.objects.get(id=checklist_id)
        items = checklist.checklistitem_set.all()
        # loop through old items and uncheck all
        for item in items:
            item.is_packed = False
            item.box_ref = ""
            item.save()

        # loop through checked items and update db
        for item in request.POST.getlist('items'):
            i = ChecklistItem.objects.get(id=item)
            # compute name holding refs
            item_name = "item_" + item
            if request.POST.get(item_name):
                i.box_ref = request.POST.get(item_name)
            i.is_packed = True
            i.save()

        text = "Packlist Saved"
        messages.add_message(request, messages.INFO, text)
        return redirect(self.success_url.format(self.get_object().id))

    def get(self, request, *args, **kwargs):
        move = self.get_object()
        items = Checklist.objects.get(move=move).checklistitem_set.all()
        payload = {
            'move': move,
            'items': items

        }
        return render(request, 'moves/move_packlist.html', payload)


class MoveDetailsView(GetMoveObjMixin, generic.edit.FormView):
    success_url = '/moves/{}/details/'
    template_name = 'moves/move_further_details.html'
    form_class = MoveDetailsForm
    pk_url_kwarg = 'move_id'
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_move))
    def dispatch(self, *args, **kwargs):
        return super(MoveDetailsView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        move = self.get_object()
        if form.is_valid():
            move.departure_from_office = form.cleaned_data[
                'departure_from_office']
            move.arrival_at_office = form.cleaned_data['arrival_at_office']
            move.speedometer_in = form.cleaned_data['speedometer_in']
            move.speedometer_out = form.cleaned_data['speedometer_out']
            move.fuel_intake = form.cleaned_data['fuel_intake']
            move.save()

            text = "Move Details Saved"
            messages.add_message(self.request, messages.INFO, text)
            return redirect(self.success_url.format(move.id))

    def get_context_data(self, **kwargs):
        ctx = super(MoveDetailsView, self).get_context_data(**kwargs)
        move = self.get_object()
        payload = {
            'move': move,
        }
        fields = self.form_class.base_fields.keys()
        form_dt = {}

        for field in fields:
            value = getattr(move, field)

            if value:
                if field in ['departure_from_office', 'arrival_at_office']:
                    #  format datetime
                    value = value.strftime('%m/%d/%Y %I:%M %p')
                form_dt[field] = value
        if form_dt:
            ctx['form'] = self.form_class(form_dt)
        ctx.update(payload)
        return ctx


class MoveDelightView(GetMoveObjMixin, generic.View):
    success_url = '/moves/{}/delight/'
    pk_url_kwarg = 'move_id'
    template_name = 'moves/move_delight_form.html'
    obj = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_move))
    def dispatch(self, *args, **kwargs):
        return super(MoveDelightView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = DelightForm(request.POST)
        if form.is_valid():
            move = self.get_object()
            if not move.token == form.cleaned_data['token']:
                text = "Customer token did not match"
                messages.add_message(request, messages.ERROR, text)
                return redirect(self.success_url.format(move.id))
            delight = move.delight
            delight.smartness = form.cleaned_data['smartness']
            delight.time = form.cleaned_data['time']
            delight.courtesy = form.cleaned_data['courtesy']
            delight.creativity = form.cleaned_data['creativity']
            delight.explanation = form.cleaned_data['explanation']
            delight.willingness = form.cleaned_data['willingness']
            delight.leader_competence = form.cleaned_data['leader_competence']
            delight.team_competence = form.cleaned_data['team_competence']
            delight.care_attention = form.cleaned_data['care_attention']
            delight.satisfaction = form.cleaned_data['satisfaction']
            delight.comments = form.cleaned_data['comments']
            delight.total = int(form.cleaned_data['smartness']) + int(form.cleaned_data['time']) + int(form.cleaned_data['courtesy']) + int(form.cleaned_data['creativity']) + int(form.cleaned_data['explanation']) + int(form.cleaned_data['willingness']) + int(form.cleaned_data['leader_competence']) + int(form.cleaned_data['team_competence']) + int(form.cleaned_data['care_attention']) + int(form.cleaned_data['satisfaction'])
            delight.save()

            move.arrival_at_client = form.cleaned_data['arrival_at_client']
            move.departure_from_client = form.cleaned_data[
                'departure_from_client'
            ]
            move.move_status = MoveStatus.objects.get(name="complete")

            move.save()

            # log but check if there is a previous entry
            if MoveLogs.objects.filter(Q(move=move) & Q(move_status=MoveStatus.objects.get(name="complete"))).exists():
                pass
            else:
                log = MoveLogs()
                log.move_status = MoveStatus.objects.get(name="complete")
                log.move = move
                log.move_rep = request.user
                log.save()
            # send delight form to user
            context = {
                'move': move,
                'datetime': datetime.now(),
                'host': request.get_host()
            }

            payload = {
                'move': move
            }

            delight_temp = rendering.render_to_pdf(
                'moves/pdf/delight_form_user.html', payload)

            data = {
                'plaintext': 'moves/emails/delight_complete.txt',
                'html': 'moves/emails/delight_complete.html',
                'context': context,
                'subject': 'Cubemovers Delight Form',
                'from': settings.EMAIL_HOST_USER,
                'to': move.customer.user.email,
                'delight': delight_temp,
                'cc': settings.CUBEMOVERS['quality_email']
            }
            send_email.delay(**data)

            text = "Delight form saved. Move Complete!"
            messages.add_message(request, messages.INFO, text)
            return redirect(self.success_url.format(move.id))
        else:
            return render(request, self.template_name, {
                'move': self.get_object(),
                'form': form
            })

    def get(self, request, *args, **kwargs):
        move = self.get_object()
        payload = {
            'move': move
        }
        return render(request, self.template_name, payload)


class PremoveListView(DatatableView):
    model = Move
    template_name = 'moves/pre-move/list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Proposed Move Date", 'get_formatted_move_date'),
            ("Created Time", 'get_formatted_datetime')
        ],
        'ordering': ['survey__move_time']
    }

    @method_decorator(user_passes_test(can_view_pre_move))
    def dispatch(self, *args, **kwargs):
        return super(PremoveListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "pre-move", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(PremoveListView, self).get_context_data(*args, **kwargs)
        context['premove_show'] = True
        return context


class MovesListView(DatatableView):
    model = Move
    template_name = 'moves/moves_list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Proposed Move Date", 'get_formatted_move_date'),
            ("Created Time", 'get_formatted_datetime')
        ],
        'ordering': ['survey__move_time']
    }

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_move))
    def dispatch(self, *args, **kwargs):
        return super(MovesListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "move", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(MovesListView, self).get_context_data(*args, **kwargs)
        context['move_list_show'] = True
        return context


class PostMovesListView(DatatableView):
    model = Move
    template_name = 'moves/post-move/list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Proposed Move Date", 'get_formatted_move_date'),
            ("Created Time", 'get_formatted_datetime')
        ],
        'ordering': ['survey__move_time']
    }

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_post_move))
    def dispatch(self, *args, **kwargs):
        return super(PostMovesListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "post-move", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(PostMovesListView, self).get_context_data(*args, **kwargs)
        context['postmove_show'] = True
        return context


class CancelledMovesListView(DatatableView):
    model = Move
    template_name = 'moves/cancelled_list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Proposed Move Date", 'get_formatted_move_date'),
            ("Created Time", 'get_formatted_datetime')
        ],
        'ordering': ['survey__move_time']
    }

    @method_decorator(user_passes_test(can_view_move))
    def dispatch(self, *args, **kwargs):
        return super(CancelledMovesListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "cancelled", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(CancelledMovesListView, self).get_context_data(*args, **kwargs)
        context['move_cancelled_show'] = True
        return context


class CompleteMovesListView(DatatableView):
    model = Move
    template_name = 'moves/complete_list.html'

    datatable_options = {
        'columns': [
            ("Move ID", 'id', helpers.link_to_model),
            ("Customer Name", 'customer__full_name'),
            ("Proposed Move Date", 'get_formatted_move_date'),
            ("Created Time", 'get_formatted_datetime')
        ],
        'ordering': ['survey__move_time']
    }

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_complete_move))
    def dispatch(self, *args, **kwargs):
        return super(CompleteMovesListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "complete", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(CompleteMovesListView, self).get_context_data(*args, **kwargs)
        context['complete_show'] = True
        return context
