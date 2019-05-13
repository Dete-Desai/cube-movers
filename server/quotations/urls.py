from django.conf.urls import url
from .views import (
    QuotationDetailView, SendQuotationView, QuotationApprovalView,
    QuotationRejectionView, QuotationsListView,
    RejectedQuotationsListView, AddSurveyQuotationView,
    AddQuotationMoveDateView, EditSurveyQuotationsItemView,
    DeleteSurveyQuotationsItemView, AddQuotationsParametersView,
    EditQuotationsView, LocalQuotePdfView)

urlpatterns = [
    url(r'^(?P<pk>\d*)/$', QuotationDetailView.as_view(), name='view'),
    url(r'^(?P<move_id>\d*)/edit/$', EditQuotationsView.as_view(), name='edit'),
    url(r'^(?P<move_id>\d*)/preview/$', LocalQuotePdfView.as_view(), name='preview'),
    url(r'^(?P<pk>\d*)/send/$', SendQuotationView.as_view(), name='send'),
    url(r'^approve/$', QuotationApprovalView.as_view(), name='approve'),
    url(r'^reject/$', QuotationRejectionView.as_view(), name='reject'),
    url(r'^list/$', QuotationsListView.as_view(), name='list'),
    url(r'^rejected/list/$', RejectedQuotationsListView.as_view(), name='rejected_list'),
    url(r'^(?P<pk>\d*)/survey/add/$', AddSurveyQuotationView.as_view(), name='add_survey'),
    url(r'^(?P<pk>\d*)/date/add/$', AddQuotationMoveDateView.as_view(), name='add_quote_date'),
    url(r'^(?P<pk>\d*)/survey/edit/$', EditSurveyQuotationsItemView.as_view(), name='edit_survey'),
    url(r'^(?P<pk>\d*)/survey/delete/$', DeleteSurveyQuotationsItemView.as_view(), name='delete_survey'),
    url(r'^(?P<pk>\d*)/parameters/add/$', AddQuotationsParametersView.as_view(), name='params_add'),
]
