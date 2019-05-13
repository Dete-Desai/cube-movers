from django.views import generic
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from datatableview.views import DatatableView
from datatableview import helpers
from core.models import (
    Move, MoveStatus, MoveLogs, MoveTeam, TraineeTeam)
from core.permissions import (
    can_view_invoice,
)
from core.utils import filter_queryset


class ConfirmInvoiceView(generic.View):

    success_url = '/inquiry/{}/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_invoice))
    def dispatch(self, *args, **kwargs):
        return super(ConfirmInvoiceView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        move.move_status = MoveStatus.objects.get(name="pre-move")
        move.save()

        # log but check if there is a previous entry
        if MoveLogs.objects.filter(Q(move=move) & Q(move_status=MoveStatus.objects.get(name="pre-move"))).exists():
            pass
        else:
            log = MoveLogs()
            log.move_status = MoveStatus.objects.get(name="pre-move")
            log.move = move
            log.move_rep = request.user
            log.save()

        # create MoveTeam, TraineeTeam, MoveVehicle, Packlist
        move.move_team = MoveTeam.objects.create()
        move.trainee_team = TraineeTeam.objects.create()
        move.save()

        text = "Invoice confirmed. Now in Premove phase"
        messages.add_message(request, messages.INFO, text)
        return redirect(self.success_url.format(move.id))


class InvoiceListView(DatatableView):
    model = Move
    template_name = 'invoices/invoice_list.html'

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
    @method_decorator(user_passes_test(can_view_invoice))
    def dispatch(self, *args, **kwargs):
        return super(InvoiceListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return filter_queryset(
            user, "invoice", "core.can_view_unassigned_move")

    def get_context_data(self, *args, **kwargs):
        context = super(InvoiceListView, self).get_context_data(*args, **kwargs)
        context['invoice_show'] = True
        return context
