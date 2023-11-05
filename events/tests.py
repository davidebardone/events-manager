import json
from datetime import date, timedelta

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient 

from .models import Event, EventRegistration

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
        user1 = UserModel.objects.get(username=json.loads(response.content)['username'])
        
        response = client.post(reverse('user_create'), userdata2, format='json')
        user2 = UserModel.objects.get(username=json.loads(response.content)['username'])

        cls.user1 = user1
        cls.user2 = user2

        # test events
        cls.event1 = Event.objects.create(
            name='Event',
            desc='Description of a wonderful event',
            start_date=date.today(),
            end_date=date.today(),
            max_capacity=2,
            author=user1
        )
        cls.event2 = Event.objects.create(
            name='Second Event',
            desc='Description of another wonderful event',
            start_date=date.today()+timedelta(days=1),
            end_date=date.today()+timedelta(days=2),
            max_capacity=1,
            author=user2
        )
        cls.pastevent = Event.objects.create(
            name='Old Event',
            desc='Description of an old past event',
            start_date=date.today()-timedelta(days=10),
            end_date=date.today()-timedelta(days=9),
            max_capacity=20,
            author=user2
        )

        # make a registration to a past event for user 2
        EventRegistration.objects.create(attendee=cls.user2, event=cls.pastevent)

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
        
        # get user 1 events
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(reverse('events_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    
    def test_list_filtered_events(self):
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # only today events
        response = client.get(f"{reverse('events_list')}?date={str(date.today())}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        # past events
        response = client.get(f"{reverse('events_list')}?is_past=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        # future events
        response = client.get(f"{reverse('events_list')}?is_future=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        # past and future
        response = client.get(f"{reverse('events_list')}?is_future=true&is_past=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)
    
    
    def test_list_my_events(self):
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
        response = client.get(reverse('my_events_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # get user 1 events
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(reverse('my_events_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertTrue(data[0]['is_author'])


    def test_get_event(self):
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
        response = client.get(reverse('event_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # get a specific event
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(reverse('event_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data['name'], self.event1.name)

        # check wrong id
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(reverse('event_detail', kwargs={'pk': 1_000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_create_event(self):
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
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


    def test_edit_event(self):
        new_data = {
            'name': 'Wonderful event [EDITED]',
            'desc': 'What a wonderful event, once in a lifetime! [EDITED]',
            'start_date': date.today()+timedelta(days=10),
            'end_date': date.today()+timedelta(days=10)
        }
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
        response = client.put(reverse('event_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try to edit an event when user is not author 
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.put(reverse('event_detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # update event 
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.put(
            reverse('event_detail', kwargs={'pk': 1}),
            data=new_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['name'], new_data['name'])
        
        # patch event 
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.patch(
            reverse('event_detail', kwargs={'pk': 1}),
            data={'name': 'patched'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['name'], 'patched')


    def test_register_to_event(self):
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # check unexisting event
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1_000}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # user 1 registers to event 1
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # user 2 registers to event 1
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # user 2 registers to event 2
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = client.post(reverse('event_registration', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # check event 1 attendees
        response = client.get(reverse('event_detail', kwargs={'pk': 1}))
        data = json.loads(response.content)
        self.assertEqual(len(data['attendees']), 2)
        self.assertEqual(
            [attendee['attendee']['username'] for attendee in data['attendees']],
            [self.user1.username, self.user2.username]
        )

        # check max capacity
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('event_registration', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('maximum capacity' in str(response.content).lower())

        # check duplicated registration
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('already registered' in str(response.content).lower())

        # chek registration to a past event
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('event_registration', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('already started' in str(response.content).lower())


    def test_unregister_to_event(self):
        # check unauthorized
        client.credentials(HTTP_AUTHORIZATION=f'Bearer xxx')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # check unexisting event
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.delete(reverse('event_registration', kwargs={'pk': 1_000}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # user 1 registers to event 1
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # user 2 registers to event 1
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = client.post(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # unregister from an not registered event
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.delete(reverse('event_registration', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # user 1 unregisters from event 1
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.delete(reverse('event_registration', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check event 1 attendees
        response = client.get(reverse('event_detail', kwargs={'pk': 1}))
        data = json.loads(response.content)
        self.assertEqual(len(data['attendees']), 1)
        self.assertEqual(
            [attendee['attendee']['username'] for attendee in data['attendees']],
            [self.user2.username]
        )

        # unregister user 2 to a past event
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = client.delete(reverse('event_registration', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('already started' in str(response.content).lower())
