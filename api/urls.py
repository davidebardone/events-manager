# api/urls.py

from django.urls import path

from .views import EventsAPIView


urlpatterns = [
    path('', EventAPIView.as_view())
]