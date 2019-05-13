from django.conf.urls import url
from .views import (
    MoveTeamView, DeleteMoveTeamMemberView,
    MoveTraineesView, DeleteMoveTraineesView,
    MoveVehiclesView, DeleteMoveVehiclesView,
    PremoveReport, ConfirmMoveView, MovePacklistView,
    MoveDetailsView, MoveDelightView,
    PremoveListView, MovesListView,
    PostMovesListView, CancelledMovesListView,
    CompleteMovesListView, CancelMoveView,
    MoveTeamLeadView)

urlpatterns = [
    url(r'^(?P<move_id>\d*)/team/$', MoveTeamView.as_view(), name='team'),
    url(r'^(?P<move_id>\d*)/cancel/$', CancelMoveView.as_view(), name='cancel'),
    url(r'^(?P<move_id>\d*)/team/(?P<member_id>\d*)/$', DeleteMoveTeamMemberView.as_view(), name='delete_member'),
    url(r'^(?P<move_id>\d*)/team_lead/$', MoveTeamLeadView.as_view(), name='add_team_lead'),
    url(r'^(?P<move_id>\d*)/trainees/$', MoveTraineesView.as_view(), name='trainees'),
    url(r'^(?P<move_id>\d*)/trainees/(?P<member_id>\d*)/$', DeleteMoveTraineesView.as_view(), name='delete_trainee'),
    url(r'^(?P<move_id>\d*)/vehicles/$', MoveVehiclesView.as_view(), name='vehicles'),
    url(r'^(?P<move_id>\d*)/vehicles/(?P<vehicle_id>\d*)/$', DeleteMoveVehiclesView.as_view(), name='delete_vehicle'),
    url(r'^(?P<move_id>\d*)/reports/(?P<report_type>[^/]+)/$', PremoveReport.as_view(), name='reports'),
    url(r'^(?P<move_id>\d*)/confirm/(?P<state>[^/]+)/$', ConfirmMoveView.as_view(), name='confirm'),
    url(r'^(?P<move_id>\d*)/packlist/(?P<checklist_id>\d*)/$', MovePacklistView.as_view(), name='packlist'),
    url(r'^(?P<move_id>\d*)/details/$', MoveDetailsView.as_view(), name='details'),
    url(r'^(?P<move_id>\d*)/delight/$', MoveDelightView.as_view(), name='delight'),
    url(r'^premoves/list/$', PremoveListView.as_view(), name='premoves_list'),
    url(r'^list/$', MovesListView.as_view(), name='list'),
    url(r'^postmoves/list/$', PostMovesListView.as_view(), name='postmoves_list'),
    url(r'^cancelled/list/$', CancelledMovesListView.as_view(), name='cancelled_list'),
    url(r'^complete/list/$', CompleteMovesListView.as_view(), name='complete_list'),
]
