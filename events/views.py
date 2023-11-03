from rest_framework import generics

from events.models import Event

from .serializers import EventSerializer
from .permissions import isAuthorOrReadOnly


class ListEventAPIView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all existing events.

    post:
    Create a new event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class DetailEventAPIView(generics.RetrieveUpdateAPIView):
    """
    get:
    Get a specific event and its details.

    put:
    Update a specific event (if it's not started yet)
    
    patch:
    Update a specific event (if it's not started yet)
    """
    permission_classes = (isAuthorOrReadOnly,)  # enable editing only for the author
    queryset = Event.objects.all()
    serializer_class = EventSerializer



