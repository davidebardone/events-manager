import json

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient 


UserModel = get_user_model()

client = APIClient()


class UserCreationTest(TestCase):

    def test_user_creation(self):
        userdata = {
            'username': 'user1',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': '$tr0ngP455w0rd!'
        }
        response = client.post(reverse('user_create'), userdata, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res_data = json.loads(response.content)
        self.assertEqual(res_data['username'], userdata['username'])
        self.assertEqual(res_data['first_name'], userdata['first_name'])
        self.assertEqual(res_data['last_name'], userdata['last_name'])
        
        # check error with already existing username
        response = client.post(reverse('user_create'), userdata, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_creation_missing_params(self):
        # check errors when mandatory params are missing
        response = client.post(reverse('user_create'), {'username': 'user1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = client.post(reverse('user_create'), {'password': 'password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class UserAuthTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create a shared test user
        cls.testuserdata = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 't3stp4ssw0rd'
        }
        client.post(reverse('user_create'), cls.testuserdata, format='json')


    def test_user_login(self):
        
        # check login endpoint
        response = client.post(
            reverse('token_obtain_pair'),
            data={
                'username': self.testuserdata['username'],
                'password': self.testuserdata['password']
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(response.content)
        self.assertTrue('access' in res_data)
        self.assertTrue('refresh' in res_data)
        
        # check token verification
        response = client.post(
            reverse('token_verify'),
            data={ 'token': res_data['access'] },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_refresh_token(self):
        # login
        response = client.post(
            reverse('token_obtain_pair'),
            data={
                'username': self.testuserdata['username'],
                'password': self.testuserdata['password']
            },
            format='json'
        )

        # check refresh token endpoint
        refresh_token = json.loads(response.content)['refresh']
        response = client.post(
            reverse('token_refresh'),
            data={ 'refresh': refresh_token },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(response.content)
        self.assertTrue('access' in res_data)
