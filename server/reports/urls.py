from django.conf.urls import url
from .views import (
    ReportsView, MovesReport, MovesComparisonReport,
    QuotationsPendingReport, QuotationsTurnAroundReport,
    BookingOrderReport, RemovalReport, PersonnelAndTransportReport,
    DelightReport)

urlpatterns = [
    url(r'^$', ReportsView.as_view(), name='reports'),
    url(r'^moves/$', MovesReport.as_view(), name='moves'),
    url(r'^moves/comparison/$', MovesComparisonReport.as_view(), name='moves_comparison'),
    url(r'^moves/removal/$', RemovalReport.as_view(), name='removal'),
    url(r'^moves/personnel_transport/$', PersonnelAndTransportReport.as_view(), name='personnel_transport'),
    url(r'^quotations/pending/$', QuotationsPendingReport.as_view(), name='quotations_pending'),
    url(r'^quotations/turnaround/$', QuotationsTurnAroundReport.as_view(), name='quotations_turnaround'),
    url(r'^booking_order/$', BookingOrderReport.as_view(), name='booking_order'),
    url(r'^delight/$', DelightReport.as_view(), name='delight'),

]
