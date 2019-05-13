from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.db.models import Q, Count
from django.shortcuts import render
from django.contrib.auth.models import User
from core.models import(
    MoveLogs, MoveStatus, Customer, MoveType, Source,
    Quotation)
from .forms import (
    MovesReportForm, MovesReportComparisonForm,
    ReportQuotationsPendingForm, ReportQuotationsTurnaroundTimeForm,
    ReportBookingOrdersForm, ReportRemovalForm, ReportPersonnelTransportForm,
    ReportDelightForm)


class ReportsView(generic.View):
    template_name = 'reports/base.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(ReportsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MovesReport(generic.View):
    template_name = 'reports/moves_report.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(MovesReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        payload = {
            'data': [0],
            'statuses': MoveStatus.objects.all().order_by('id'),
            'employees': employees,
            'sources': Source.objects.all(),
            'move_types': MoveType.objects.filter(is_active=True)
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = MovesReportForm(request.POST)
        if form.is_valid():
            move_status = form.cleaned_data['move_status']
            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            frequency = form.cleaned_data['frequency']
            move_rep = form.cleaned_data['move_rep']
            source_id = form.cleaned_data['source']
            type_id = form.cleaned_data['move_type']
            if move_rep == 0:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name=move_status)) & Q(timestamp__range=(from_time, to_time)))
            else:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name=move_status)) & Q(timestamp__range=(from_time, to_time)) & Q(move__move_rep=move_rep))

            if source_id is not 0:
                moves = moves.filter(move__customer__source=source_id)

            if type_id is not 0:
                moves = moves.filter(move__move_type=type_id)

            labels = list()
            count = list()

            if frequency == 'daily':
                move_groups = moves.values('timestamp').annotate(count_items=Count('timestamp'))
                for move in move_groups:
                    labels.append(str(move['timestamp']))
                    count.append(move['count_items'])

            elif frequency == 'monthly':
                move_groups = moves.extra(select={'month': "EXTRACT(month FROM timestamp)", 'year': "EXTRACT(year FROM timestamp)"}).values('month', 'year').annotate(count_items=Count('timestamp'))
                for move in move_groups:
                    labels.append(str(move['month']) + '/' + str(move['year']))
                    count.append(move['count_items'])

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)

            payload = {
                'labels': labels,
                'data': count,
                'moves': moves,
                'statuses': MoveStatus.objects.all().order_by('id'),
                'employees': employees,
                'sources': Source.objects.all(),
                'move_types': MoveType.objects.filter(is_active=True),
                'old': request.POST
            }

            # return render(request, 'core/test.html', payload)
            return render(request, self.template_name, payload)


class MovesComparisonReport(generic.View):
    template_name = 'reports/moves_comparison_report.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(MovesComparisonReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        # g = Group.objects.get(name='move rep')
        # surveyors = g.user_set.all()

        payload = {
            'data': [0],
            'statuses': MoveStatus.objects.all().order_by('id'),
            'employees': employees,
            'sources': Source.objects.all()
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = MovesReportComparisonForm(request.POST)

        if form.is_valid():
            move_status_1 = form.cleaned_data['move_status_1']
            move_status_2 = form.cleaned_data['move_status_2']
            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            # frequency = form.cleaned_data['frequency']
            move_rep = form.cleaned_data['move_rep']

            if move_rep == 0:
                moves_1 = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name=move_status_1)) & Q(timestamp__range=(from_time, to_time)))
                moves_2 = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name=move_status_2)) & Q(timestamp__range=(from_time, to_time)))
            else:
                moves_1 = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name=move_status_1)) & Q(timestamp__range=(from_time, to_time)) & Q(move__move_rep=move_rep))
                moves_2 = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name=move_status_2)) & Q(timestamp__range=(from_time, to_time)) & Q(move__move_rep=move_rep))

            labels = list()
            labels.append(str(move_status_1))
            labels.append(str(move_status_2))

            count = list()
            count.append(moves_1.count())
            count.append(moves_2.count())

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)
            # return HttpResponse(labels[0])

            payload = {
                'labels': labels,
                'data': count,
                'moves_1': moves_1,
                'moves_2': moves_2,
                'statuses': MoveStatus.objects.all().order_by('id'),
                'employees': employees,
                'old': request.POST
            }

            return render(request, self.template_name, payload)


class QuotationsPendingReport(generic.View):
    template_name = 'reports/quotations/pending.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(QuotationsPendingReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        recs = Quotation.objects.filter(status="not sent")

        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        # g = Group.objects.get(name='move rep')
        # surveyors = g.user_set.all()

        labels = list()
        count = list()

        rec_groups = recs.values('created_time').annotate(count_items=Count('created_time'))
        for rec in rec_groups:
            labels.append(str(rec['created_time']))
            count.append(rec['count_items'])

        payload = {
            'recs': recs,
            'employees': employees,
            'labels': labels,
            'data': count,
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = ReportQuotationsPendingForm(request.POST)

        if form.is_valid():
            status = form.cleaned_data['status']
            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            move_rep = form.cleaned_data['move_rep']

            if move_rep == 0:
                recs = Quotation.objects.filter(Q(status=status) & Q(created_time__range=(from_time, to_time)))
            else:
                recs = Quotation.objects.filter(Q(status=status) & Q(created_time__range=(from_time, to_time)) & Q(move_rep=move_rep))

            labels = list()
            count = list()

            rec_groups = recs.values('created_time').annotate(count_items=Count('created_time'))
            for rec in rec_groups:
                labels.append(str(rec['created_time']))
                count.append(rec['count_items'])

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)

            payload = {
                'labels': labels,
                'data': count,
                'recs': recs,
                'statuses': MoveStatus.objects.all().order_by('id'),
                'employees': employees,
                'old': request.POST
            }

            return render(request, self.template_name, payload)


class QuotationsTurnAroundReport(generic.View):
    template_name = 'reports/quotations/turnaround.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(QuotationsTurnAroundReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="quotation")) & ~Q(move__checklist__quotation__sent_time=None))
        moves = moves.extra(select={'offset': "reply_time - sent_time"})

        labels = list()
        count = list()

        for move in moves:
            labels.append(str(move.move.checklist.quotation.id))
            count.append(move.offset)

        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        # g = Group.objects.get(name='move rep')
        # surveyors = g.user_set.all()

        payload = {
            'labels': labels,
            'data': count,
            'moves': moves,
            'employees': employees,
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = ReportQuotationsTurnaroundTimeForm(request.POST)

        if form.is_valid():
            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            move_rep = form.cleaned_data['move_rep']

            if move_rep == 0:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="quotation")) & Q(timestamp__range=(from_time, to_time)) & ~Q(move__checklist__quotation__sent_time=None))
            else:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="quotation")) & Q(timestamp__range=(from_time, to_time)) & Q(move__move_rep=move_rep) & ~Q(move__checklist__quotation__sent_time=None))

            moves = moves.extra(select={'offset': "reply_time - sent_time"})

            labels = list()
            count = list()

            for move in moves:
                labels.append(str(move.move.checklist.quotation.id))
                count.append(move.offset)

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)

            payload = {
                'labels': labels,
                'data': count,
                'moves': moves,
                'employees': employees,
                'old': request.POST
            }

            return render(request, self.template_name, payload)


class BookingOrderReport(generic.View):
    template_name = 'reports/booking_order_report.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(BookingOrderReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        moves = MoveLogs.objects.filter(move_status=MoveStatus.objects.get(name="invoice"))

        labels = list()
        count = list()

        move_groups = moves.values('move_rep', 'move_rep__first_name').annotate(count_items=Count('move_rep'))

        for move in move_groups:
            labels.append(str(move['move_rep__first_name']))
            count.append(move['count_items'])

        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        # g = Group.objects.get(name='move rep')
        # surveyors = g.user_set.all()

        payload = {
            'labels': labels,
            'data': count,
            'moves': moves,
            'employees': employees,
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = ReportBookingOrdersForm(request.POST)

        if form.is_valid():

            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            move_rep = form.cleaned_data['move_rep']

            if move_rep == 0:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="invoice")) & Q(timestamp__range=(from_time, to_time)))
            else:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="invoice")) & Q(timestamp__range=(from_time, to_time)) & Q(move__move_rep=move_rep))

            labels = list()
            count = list()

            move_groups = moves.values('move_rep', 'move_rep__first_name').annotate(count_items=Count('move_rep'))

            for move in move_groups:
                labels.append(str(move['move_rep__first_name']))
                count.append(move['count_items'])

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)

            payload = {
                'labels': labels,
                'data': count,
                'moves': moves,
                'employees': employees,
                'old': request.POST
            }

            return render(request, self.template_name, payload)


class RemovalReport(generic.View):
    template_name = 'reports/removal_report.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(RemovalReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        moves = MoveLogs.objects.filter(move_status=MoveStatus.objects.get(name="post-move"))
        labels = list()
        count = list()
        move_groups = moves.values('move_rep', 'move_rep__first_name').annotate(count_items=Count('move_rep'))

        for move in move_groups:
            labels.append(str(move['move_rep__first_name']))
            count.append(move['count_items'])

        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        # g = Group.objects.get(name='move rep')
        # surveyors = g.user_set.all()

        payload = {
            'labels': labels,
            'data': count,
            'moves': moves,
            'employees': employees,
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = ReportRemovalForm(request.POST)
        if form.is_valid():

            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            move_rep = form.cleaned_data['move_rep']

            if move_rep == 0:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="post-move")) & Q(move__move_date__range=(from_time, to_time)))
            else:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="post-move")) & Q(move__move_date__range=(from_time, to_time)) & Q(move__move_rep=move_rep))

            labels = list()
            count = list()

            move_groups = moves.values('move_rep', 'move_rep__first_name').annotate(count_items=Count('move_rep'))

            for move in move_groups:
                labels.append(str(move['move_rep__first_name']))
                count.append(move['count_items'])

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)

            payload = {
                'labels': labels,
                'data': count,
                'moves': moves,
                'employees': employees,
                'old': request.POST
            }

            return render(request, self.template_name, payload)


class PersonnelAndTransportReport(generic.View):
    template_name = 'reports/personnel_and_transport_report.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(PersonnelAndTransportReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        moves = MoveLogs.objects.filter(move_status=MoveStatus.objects.get(name="post-move"))

        labels = list()
        count = list()

        move_groups = moves.values('move_rep', 'move_rep__first_name').annotate(count_items=Count('move_rep'))

        for move in move_groups:
            labels.append(str(move['move_rep__first_name']))
            count.append(move['count_items'])

        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        # g = Group.objects.get(name='move rep')
        # surveyors = g.user_set.all()

        payload = {
            'labels': labels,
            'data': count,
            'moves': moves,
            'employees': employees,
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = ReportPersonnelTransportForm(request.POST)

        if form.is_valid():

            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            move_rep = form.cleaned_data['move_rep']

            if move_rep == 0:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="post-move")) & Q(move__move_date__range=(from_time, to_time)))
            else:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="post-move")) & Q(move__move_date__range=(from_time, to_time)) & Q(move__move_rep=move_rep))

            labels = list()
            count = list()

            move_groups = moves.values('move_rep', 'move_rep__first_name').annotate(count_items=Count('move_rep'))

            for move in move_groups:
                labels.append(str(move['move_rep__first_name']))
                count.append(move['count_items'])

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)

            payload = {
                'labels': labels,
                'data': count,
                'moves': moves,
                'employees': employees,
                'old': request.POST
            }

            return render(request, self.template_name, payload)


class DelightReport(generic.View):
    template_name = 'reports/delight_report.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(DelightReport, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        moves = MoveLogs.objects.filter(move_status=MoveStatus.objects.get(name="complete"))

        labels = list()
        count = list()

        for move in moves:
            labels.append("MOV " + str(move.move.id))
            count.append(int(move.move.delight.total))

        customers = Customer.objects.all().values('user')
        employees = User.objects.exclude(id__in=customers)

        # g = Group.objects.get(name='move rep')
        # surveyors = g.user_set.all()

        payload = {
            'labels': labels,
            'data': count,
            'moves': moves,
            'employees': employees,
        }

        return render(request, self.template_name, payload)

    def post(self, request, *args, **kwargs):
        form = ReportDelightForm(request.POST)

        if form.is_valid():

            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            move_rep = form.cleaned_data['move_rep']

            if move_rep == 0:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="complete")) & Q(timestamp__range=(from_time, to_time)))
            else:
                moves = MoveLogs.objects.filter(Q(move_status=MoveStatus.objects.get(name="complete")) & Q(timestamp__range=(from_time, to_time)) & Q(move__move_rep=move_rep))

            labels = list()
            count = list()

            for move in moves:
                labels.append("MOV " + str(move.move.id))
                count.append(int(move.move.delight.total))

            customers = Customer.objects.all().values('user')
            employees = User.objects.exclude(id__in=customers)

            payload = {
                'labels': labels,
                'data': count,
                'moves': moves,
                'employees': employees,
                'old': request.POST
            }

            return render(request, self.template_name, payload)
