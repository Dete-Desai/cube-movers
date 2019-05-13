from django.conf.urls import url
from .views import (
    ConfirmInvoiceView, InvoiceListView)

urlpatterns = [
    url(r'^(?P<move_id>\d*)/confirm/$', ConfirmInvoiceView.as_view(), name='confirm'),
    url(r'^list/$', InvoiceListView.as_view(), name='list'),
]
