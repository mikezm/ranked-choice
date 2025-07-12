from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('ballots/', views.create_ballot, name='create_ballot'),
    path('ballots/all/', views.list_ballots, name='list_ballots'),
    path('ballots/<slug:slug>/', views.get_ballot, name='get_ballot'),
    path('ballots/results/<slug:slug>/', views.get_votes, name='get_votes'),
    path('vote/', views.create_vote, name='create_vote'),
]
