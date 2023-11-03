from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from events.models import Event, EventRegistration

from .serializers import EventSerializer, EventRegistrationSerializer
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


class RegisterToEventAPIView(APIView):
    serializer_class = EventRegistrationSerializer

    def post(self, request, pk, *args, **kwargs):
        """
        Register to a specific event as an attendee
        """
        event = get_object_or_404(Event, pk=pk)
        serializer = EventRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(attendee=request.user, event=event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListMyEventsAPIView(generics.ListAPIView):
    """
    List all events created by the current user
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(author=user)


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

