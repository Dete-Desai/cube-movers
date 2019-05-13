from django.conf.urls import include, url
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^$', include('dashboard.urls', namespace='dashboard')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^customers/', include('customers.urls', namespace='customers')),
    url(r'^inquiry/', include('inquiries.urls', namespace='inquiry')),
    url(r'^surveys/', include('surveys.urls', namespace='surveys')),
    url(r'^quotations/', include('quotations.urls', namespace='quotations')),
    url(r'^moves/', include('moves.urls', namespace='moves')),
    url(r'^invoices/', include('invoices.urls', namespace='invoices')),
    url(r'^bookings/', include('bookings.urls', namespace='bookings')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^login/$', views.account_login, name='account_login'),
    url(r'^logout/$', views.account_logout, name='account_logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'helpdesk/', include('helpdesk.urls')),
]
