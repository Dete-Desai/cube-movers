from django.conf.urls import url
from .views import (
    ListCustomersView, CreateCustomersView, CustomerDetailView,
    CustomerUpdateView)

urlpatterns = [
    url(r'^$', ListCustomersView.as_view(), name='list'),
    url(r'^create/$', CreateCustomersView.as_view(), name='create'),
    url(r'^(?P<pk>\d*)/$', CustomerDetailView.as_view(), name='view'),
    url(r'^update/(?P<pk>\d*)/$', CustomerUpdateView.as_view(), name='update')
]
