from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.models import Event, EventRegistration


UserModel = get_user_model()


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "username",
            "first_name",
            "last_name"
        ]


class EventSerializer(serializers.ModelSerializer):
    attendees = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = ("id", "name", "desc", "start_date", "end_date", "attendees")


    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError("start_date must be <= than end_date")
        return attrs


    def create(self, validated_data):
        event = Event(**validated_data, author=self.context['request'].user)
        event.save()
        return event


    def get_attendees(self, obj):
        qs = EventRegistration.objects.filter(event=obj)
        try:
            serializer = EventRegistrationSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ('id',)
