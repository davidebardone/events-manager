from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model # use custom user model

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    Create a new user account
    """
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # so that anonimous users can register
    ]
    serializer_class = UserSerializer