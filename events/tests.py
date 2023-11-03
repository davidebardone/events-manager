import json
from datetime import date, timedelta

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient 

from .models import Event

UserModel = get_user_model()

client = APIClient()


class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # test user
        userdata = {
            'username': 'user1',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': '$tr0ngP455w0rd!'
        }
        userdata2 = userdata.copy()
        userdata2['username'] = 'user2'
        
        response = client.post(reverse('user_create'), userdata, format='json')
        user1 = UserModel.objects.get(pk=json.loads(response.content)['id'])
        
        response = client.post(reverse('user_create'), userdata2, format='json')
        user2 = UserModel.objects.get(pk=json.loads(response.content)['id'])
        
        # test events
        cls.event1 = Event.objects.create(
            name='Event',
            desc='Description of a wonderful event',
            start_date=date(2023, 12, 25),
            end_date=date(2023, 12, 26),
            author = user1
        )
        cls.event2 = Event.objects.create(
            name='Second Event',
            desc='Description of another wonderful event',
            start_date=date(2024, 12, 25),
            end_date=date(2024, 12, 26),
            author = user2
        )

        # login and save jwt access tokens
        response = client.post(
            reverse('token_obtain_pair'),
            {'username': userdata['username'], 'password': userdata['password']},
            format='json'
        )
        cls.token = json.loads(response.content)['access']
        response = client.post(
            reverse('token_obtain_pair'),
            {'username': userdata2['username'], 'password': userdata2['password']},
            format='json'
        )
        cls.token2 = json.loads(response.content)['access']


    def test_list_event(self):
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
        response = client.get(reverse('events_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # get events
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(reverse('events_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)


    def test_get_event(self):
        # get a specific event
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(reverse('event_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data['name'], self.event1.name)

    
    def test_create_event(self):
        # check unauthorized
        response = client.post(reverse('events_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # create event
        event_data = {
            'name': 'Wonderful event',
            'desc': 'What a wonderful event, once in a lifetime!',
            'start_date': date.today(),
            'end_date': date.today()
        }
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('events_list'), event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data['name'], event_data['name'])
        self.assertEqual(data['desc'], event_data['desc'])
        self.assertEqual(data['start_date'], str(event_data['start_date']))
        self.assertEqual(data['end_date'], str(event_data['end_date']))

        # create event with start > end, check validation error
        event_data['start_date'] = event_data['end_date'] + timedelta(days=1)
        response = client.post(reverse('events_list'), event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        self.assertTrue('non_field_errors' in data)


    def test_list_my_events(self):
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
        response = client.get(reverse('my_events_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # get events
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(reverse('my_events_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)


    def test_register_to_event(self):
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
