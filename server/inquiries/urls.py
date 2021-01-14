from django.urls import include, path
from .views import (
    InquiryListView, InquiryDetailView, InquiryCreateView,
    InquiryDetailsCreateView, CustomerUpdateView)

urlpatterns = [
    path('', InquiryListView.as_view(), name='list'),
    path('(?P<pk>\d*)/$', InquiryDetailView.as_view(), name='view'),
    path('new/(?P<customer_id>\d*)/$', InquiryCreateView.as_view(), name='create'),
    path('(?P<pk>\d*)/property/new/$', InquiryDetailsCreateView.as_view(), name='add_property'),
    path('(?P<pk>\d*)/property/update/$', CustomerUpdateView.as_view(), name='edit_property')
]
