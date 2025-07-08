from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    # Add API endpoints here
    path('health/', views.health_check, name='health_check'),
    path('ballots/', views.create_ballot, name='create_ballot'),
    path('ballots/<slug:slug>/', views.get_ballot, name='get_ballot'),
    path('vote/', views.create_vote, name='create_vote'),
]
