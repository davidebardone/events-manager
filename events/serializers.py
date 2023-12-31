from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from events.models import Event, EventRegistration


UserModel = get_user_model()


class AttendeeSerializer(serializers.ModelSerializer):
    '''
    Used to add attendees information inside the EventRegistrationSerializer
    '''
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
    is_attendee = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id", "name", "desc", "start_date", "end_date",
            "is_author", "is_attendee", "attendees", "max_capacity"
        )


    def validate(self, attrs):
        # check if dates are coherent (start before or same as end)
        if ('start_date' in attrs and 'end_date' in attrs and
            attrs['start_date'] > attrs['end_date']):
            raise serializers.ValidationError("start_date must be before or same as end_date")
        return attrs


    def create(self, validated_data):
        # use currently logged user as author
        event = Event(**validated_data, author=self.context['request'].user)
        event.save()
        return event


    def get_attendees(self, obj):
        # get list of all registered attendees
        qs = EventRegistration.objects.filter(event=obj)
        try:
            serializer = EventRegistrationSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data
    

    def get_is_author(self, obj) -> bool:
        # is current logged user the author
        user = self.context['request'].user
        return obj.author == user


    def get_is_attendee(self, obj) -> bool:
        # is current logged user among registered attendees
        user = self.context['request'].user
        return EventRegistration.objects.filter(
            event=obj, attendee=user
        ).exists()


class EventFilterSerializer(serializers.Serializer):
    """
    Serializer used for query params validation
    """
    mine = serializers.BooleanField(required=False)
    date = serializers.DateField(required=False)
    is_past = serializers.BooleanField(required=False)
    is_future = serializers.BooleanField(required=False)


class EventRegistrationSerializer(serializers.ModelSerializer):
    
    attendee = AttendeeSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ('attendee', )