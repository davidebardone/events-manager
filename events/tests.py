from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Event

UserModel = get_user_model()


class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserModel.objects.create(
            username='User1',
            first_name='Test',
            last_name='User',
            password='strong_password'
        )
        Event.objects.create(
            name='Event',
            desc='Description of a wonderful event',
            start_date=date(2023, 12, 25),
            end_date=date(2023, 12, 26),
            author = user
        )

    def test_event_content(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.name, 'Event')
        self.assertEqual(event.desc, 'Description of a wonderful event')
        self.assertEqual(event.start_date, date(2023, 12, 25))
        self.assertEqual(event.end_date, date(2023, 12, 26))
        self.assertEqual(event.author.username, 'User1')
