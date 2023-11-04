from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# default user model
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ("username", "first_name", "last_name", "password")

    def validate_password(self, value: str) -> str:
        """
        Hash the password passed by user
        """
        return make_password(value)