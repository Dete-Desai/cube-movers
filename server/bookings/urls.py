from django.conf.urls import url
from .views import (
    RaiseBookingOrderView, BookingOrderDetailView, SendBookingOrderPDFEmail,
    BookingOrderPDFEmail)

urlpatterns = [
    url(r'^(?P<move_id>\d*)/raise_order/$', RaiseBookingOrderView.as_view(), name='raise_order'),
    url(r'^(?P<move_id>\d*)/$', BookingOrderDetailView.as_view(), name='booking_order'),
    url(r'^(?P<move_id>\d*)/send/$', SendBookingOrderPDFEmail.as_view(), name='send_email'),
    url(r'^(?P<move_id>\d*)/pdf/$', BookingOrderPDFEmail.as_view(), name='pdf'),
]
