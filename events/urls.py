# api/urls.py

from django.urls import path

from .views import ListEventAPIView, DetailEventAPIView


urlpatterns = [
    path('<int:pk>/', DetailEventAPIView.as_view(), name='event_detail'),
    path('', ListEventAPIView.as_view(), name='events_list'),
]