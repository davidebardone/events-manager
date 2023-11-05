from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
    is_author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = ("id", "name", "desc", "start_date", "end_date", "is_author", "attendees")


    def validate(self, attrs):
        # check if dates are coherent (start before or same as end)
        if ('start_date' in attrs and 'end_date' in attrs and
            attrs['start_date'] > attrs['end_date']):
            raise serializers.ValidationError("start_date must be before or same as end_date")
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
    

    def get_is_author(self, obj) -> bool:
        user = self.context['request'].user
        return obj.author == user


class EventFilterSerializer(serializers.Serializer):
    """
    Serializer used for query params validation
    """
    date = serializers.DateField(required=False)
    is_past = serializers.BooleanField(required=False)
    is_future = serializers.BooleanField(required=False)


class EventRegistrationSerializer(serializers.ModelSerializer):
    
    attendee = AttendeeSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ('attendee', )