from django.views import generic
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render
from easy_pdf import rendering
from django.conf import settings
from core.models import (
    Move, MoveStatus, MoveLogs, QuoteItem, QuoteItemType)
from core.permissions import (
    can_view_quotes,
)
from core.tasks import send_email as send_booking_order_email


class RaiseBookingOrderView(generic.View):

    success_url = '/inquiry/{}/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(RaiseBookingOrderView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        move.move_status = MoveStatus.objects.get(name="invoice")
        move.save()

        # log but check if there is a previous entry
        if MoveLogs.objects.filter(Q(move=move) & Q(move_status=MoveStatus.objects.get(name="invoice"))).exists():
            pass
        else:
            log = MoveLogs()
            log.move_status = MoveStatus.objects.get(name="invoice")
            log.move = move
            log.move_rep = request.user
            log.save()

        text = "Booking Order Raised"
        messages.add_message(request, messages.INFO, text)
        return redirect(self.success_url.format(move.id))


class BookingOrderDetailView(generic.DetailView):
    template_name = 'bookings/booking-order.html'
    model = Move
    pk_url_kwarg = 'move_id'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(BookingOrderDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super(BookingOrderDetailView, self).get_context_data(**kwargs)
        move = self.get_object()
        quotation = move.checklist.quotation

        vat = (quotation.vat / 100) * quotation.selling_price

        payload = {
            'move': move,
            'types': QuoteItemType.objects.all(),
            'quotation': quotation,
            'quote_items': QuoteItem.objects.filter(quotation=quotation),
            'vat': vat
        }
        cxt.update(payload)
        return cxt


class SendBookingOrderPDFEmail(generic.View):

    success_url = '/bookings/{}/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(SendBookingOrderPDFEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        quotation = move.checklist.quotation
        vat = (quotation.vat / 100) * quotation.selling_price
        payload = {
            'move': move,
            'types': QuoteItemType.objects.all(),
            'quotation': quotation,
            'quote_items': QuoteItem.objects.filter(quotation=quotation),
            'vat': vat
        }

        booking_order = rendering.render_to_pdf(
            'bookings/emails/booking_order_pdf.html', payload)

        data = {
            'plaintext': 'bookings/emails/booking_order_pdf.txt',
            'html': 'bookings/emails/booking_order_pdf.html',
            'context': {},
            'subject': 'Booking Order',
            'from': settings.EMAIL_HOST_USER,
            'to': settings.BOOKING_ORDER_EMAIL,
            'booking_order': booking_order
        }

        send_booking_order_email.delay(**data)

        return redirect(self.success_url.format(move.id))


class BookingOrderPDFEmail(generic.View):

    success_url = '/bookings/{}/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(BookingOrderPDFEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        move_id = kwargs.get('move_id')
        move = Move.objects.get(id=move_id)
        quotation = move.checklist.quotation

        vat = (quotation.vat / 100) * quotation.selling_price

        payload = {
            'move': move,
            'types': QuoteItemType.objects.all(),
            'quotation': quotation,
            'quote_items': QuoteItem.objects.filter(quotation=quotation),
            'vat': vat
        }

        return rendering.render_to_pdf_response(
            request, 'bookings/emails/booking_order_pdf.html', payload,
            filename='Booking_Order_{}.pdf'.format(move.id))
