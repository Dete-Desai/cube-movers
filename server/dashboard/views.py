from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core.models import MoveStatus, Move
from core.utils import count_records


class DashboardView(generic.View):
    template = 'dashboard/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        inquiries = count_records(user, "inquiry", "core.can_view_unassigned_move")
        pre_surveys = count_records(
            user, "pre-survey", "core.can_view_unassigned_move")
        surveys = count_records(user, "survey", "core.can_view_unassigned_move")

        invoices = count_records(user, "invoice", "core.can_view_unassigned_move")
        pre_moves = count_records(
            user, "pre-move", "core.can_view_unassigned_move")

        moves = count_records(user, "move", "core.can_view_unassigned_move")
        cancelled_moves = count_records(
            user, "cancelled", "core.can_view_unassigned_move")
        post_moves = count_records(
            user, "post-move", "core.can_view_unassigned_move")
        complete = count_records(user, "complete", "core.can_view_unassigned_move")

        if user.has_perm("core.can_view_unassigned_move"):
            quotes = Move.objects.filter(
                ~Q(checklist__quotation__status="rejected"),
                move_status=MoveStatus.objects.get(name='quotation')).count()
        else:
            quotes = Move.objects.filter(
                ~Q(checklist__quotation__status="rejected"),
                move_status=MoveStatus.objects.get(name='quotation'),
                survey__surveyor=user).count()

        if user.has_perm("core.can_view_unassigned_move"):
            rejected_quotes = Move.objects.filter(
                checklist__quotation__status="rejected",
                move_status=MoveStatus.objects.get(name='quotation')).count()
        else:
            rejected_quotes = Move.objects.filter(
                checklist__quotation__status="rejected",
                move_status=MoveStatus.objects.get(name='quotation'),
                survey__surveyor=request.user).count()

        payload = {
            'inquiries': inquiries,
            'pre_surveys': pre_surveys,
            'surveys': surveys,
            'quotes': quotes,
            'invoices': invoices,
            'pre_moves': pre_moves,
            'moves': moves,
            'post_moves': post_moves,
            'complete': complete,
            'cancelled_moves': cancelled_moves,
            'rejected_quotes': rejected_quotes,
            'overview_show': True
        }
        return render(request, self.template, payload)
