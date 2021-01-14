from django.contrib import admin
from django.urls import include, path
from django.urls import reverse
from core import views

urlpatterns = [
    #path('mfa/', include(("deux.urls", 'app_name'), namespace="mfa")),
    path('', include(('dashboard.urls','dashboard'), namespace='dashboard')),
    path('dashboard/', include(('dashboard.urls','dashboard'), namespace='dashboard')),
    path('customers/', include(('customers.urls','customers'), namespace='customers')),
    path('inquiry/', include(('inquiries.urls','inquiries'), namespace='inquiry')),
    path('surveys/', include(('surveys.urls','surveys'), namespace='surveys')),
    path('quotations/', include(('quotations.urls','quotations'), namespace='quotations')),
    path('moves/', include(('moves.urls','moves'), namespace='moves')),
    path('invoices/', include(('invoices.urls','invoices'), namespace='invoices')),
    path('bookings/', include(('bookings.urls','bookings'), namespace='bookings')),
    path('reports/', include(('reports.urls','reports'), namespace='reports')),
    path('tinymce/', include(('tinymce.urls','tinymce'))),
    path('login/$', views.account_login, name='account_login'),
    path('logout/$', views.account_logout, name='account_logout'),
    path('admin/', include(admin.site.urls)),
    path('helpdesk/', include('helpdesk.urls','helpdesk')),
]
