from django.urls import include, path
from .views import (
    ListCustomersView, CreateCustomersView, CustomerDetailView,
    CustomerUpdateView)

urlpatterns = [
    path('', ListCustomersView.as_view(), name='list'),
    path('create/$', CreateCustomersView.as_view(), name='create'),
    path('(?P<pk>\d*)/$', CustomerDetailView.as_view(), name='view'),
    path('update/(?P<pk>\d*)/$', CustomerUpdateView.as_view(), name='update')
]
