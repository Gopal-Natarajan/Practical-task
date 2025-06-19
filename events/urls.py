from django.urls import path
from . import views

urlpatterns = [
    path('', views.upcoming_events, name='upcoming_events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('past/', views.past_events, name='past_events'),
]
