# api/urls.py

from django.urls import path

from .views import (
    ListEventAPIView, DetailEventAPIView, ListMyEventsAPIView,
    RegisterToEventAPIView
)


urlpatterns = [
    path('<int:pk>/registrations', RegisterToEventAPIView.as_view(), name='event_registration'),
    path('<int:pk>/', DetailEventAPIView.as_view(), name='event_detail'),
    path('mine/', ListMyEventsAPIView.as_view(), name='my_events_list'),
    path('', ListEventAPIView.as_view(), name='events_list'),
]