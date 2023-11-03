from rest_framework import serializers
from django.contrib.auth import get_user_model

# default user model
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ( "id", "username", "first_name", "last_name", "password")