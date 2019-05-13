from django.conf.urls import url
from .views import (
    CreateSurveyView, ConfirmSurveyView, SurveyChecklistView,
    CreateSurveyDestinationView, PresurveyListView, SurveyListView,
    SurveyChecklistAddExistingItemView, SurveyChecklistAddNewItemView,
    SurveyChecklistItemDeleteView, SurveyChecklistItemEditView,
    SurveyInstructionsView)

urlpatterns = [
    url(r'^(?P<pk>\d*)/new/$', CreateSurveyView.as_view(), name='create'),
    url(r'^(?P<pk>\d*)/confirm/$', ConfirmSurveyView.as_view(), name='confirm'),
    url(r'^checklist/(?P<pk>\d*)/$', SurveyChecklistView.as_view(), name='checklist'),
    url(r'^(?P<pk>\d*)/destination/$', CreateSurveyDestinationView.as_view(), name='destination'),
    url(r'^presurvey/list/$', PresurveyListView.as_view(), name='presurvey_list'),
    url(r'^list/$', SurveyListView.as_view(), name='list'),
    url(r'^checklist/(?P<checklist_id>\d*)/add/existing/$', SurveyChecklistAddExistingItemView.as_view(),
        name='checklist_add_existing'),
    url(r'^checklist/(?P<checklist_id>\d*)/add/new/$', SurveyChecklistAddNewItemView.as_view(),
        name='checklist_add_new'),
    url(r'^checklist/(?P<checklist_id>\d*)/delete/$', SurveyChecklistItemDeleteView.as_view(),
        name='checklist_delete'),
    url(r'^checklist/(?P<checklist_id>\d*)/edit/$', SurveyChecklistItemEditView.as_view(),
        name='checklist_edit'),
    url(r'^(?P<checklist_id>\d*)/instructions/$', SurveyInstructionsView.as_view(), name='instructions'),
]
