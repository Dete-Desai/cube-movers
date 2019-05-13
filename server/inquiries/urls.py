from django.conf.urls import url
from .views import (
    InquiryListView, InquiryDetailView, InquiryCreateView,
    InquiryDetailsCreateView, CustomerUpdateView)

urlpatterns = [
    url(r'^$', InquiryListView.as_view(), name='list'),
    url(r'^(?P<pk>\d*)/$', InquiryDetailView.as_view(), name='view'),
    url(r'^new/(?P<customer_id>\d*)/$', InquiryCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d*)/property/new/$', InquiryDetailsCreateView.as_view(), name='add_property'),
    url(r'^(?P<pk>\d*)/property/update/$', CustomerUpdateView.as_view(), name='edit_property')
]
