import logging
from http import HTTPStatus

from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


class AccountUserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_user_success(self):
        data = {
            'username': 'testuser',
            "email": 'testemail@yandex.ru',
            'password': 'user12345',
            "password2": 'user12345'
        }

        response = self.client.post('/accounts/users', data)

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            user = None

        logger.info(response.json()['message'])
        logger.info("".join(["Статус код ", str(response.status_code)]))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(user, User)

    def test_registration_user_fail(self):
        data = {
            'username': 'testuserfail',
            "email": 'testemailyandex',
            'password': 'test12345',
            "password2": 'test12345'
        }

        response = self.client.post('/accounts/users', data)

        logger.info("".join(["Статус код ", str(response.status_code)]))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        data['username'] = 'soo'
        data['email'] = 'testemail@yandex.ru'

        logger.info("".join(["Статус код ", str(response.status_code)]))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response = self.client.post('/accounts/users', data)

        logger.info("".join(["Статус код ", str(response.status_code)]))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        data['username'] = 'testuserfail'
        data['password'] = '123'
        data['password2'] = '123'

        response = self.client.post('/accounts/users', data)

        logger.info("".join(["Статус код ", str(response.status_code)]))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        data['password'] = '!asdfg123'
        data['password2'] = '!asdfg12'

        response = self.client.post('/accounts/users', data)

        logger.info("".join(["Статус код ", str(response.status_code)]))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_сustom_auth_token_success(self):
        data = {
            'username': 'testuser',
            'password': 'test123',
        }

        User.objects.create_user(**data)
        response = self.client.post('/accounts/api-token-auth/', data)
        token = response.json()['token']

        logger.info("".join(["Статус код ", str(response.status_code)]))
        logger.info("".join(["Токен ", token]))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNotNone(token)

    def test_сustom_auth_token_fail(self):
        data = {
            'username': 'testuser1',
            'password': 'test123',
        }

        response = self.client.post('/accounts/api-token-auth/', data)

        logger.info("".join(["Статус код ", str(response.status_code)]))
        logger.info(response.json()['non_field_errors'])

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_authentication_success(self):
        data = {
            'username': 'testuser1',
            'password': 'test123',
        }

        User.objects.create_user(**data)
        token = self.client.post('/accounts/api-token-auth/', data, follow=True).json()['token']
        response = self.client.get('/accounts/authentication/',
                                   HTTP_AUTHORIZATION="".join(["Token ", token]),
                                   follow=True)
        username = response.json()['username']

        logger.info("".join(["Статус код ", str(response.status_code)]))
        logger.info(response.json())

        self.assertEqual(username, data['username'])
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authentication_fail(self):
        response = self.client.get('/accounts/authentication/',
                                   HTTP_AUTHORIZATION="Token ",
                                   follow=True)

        logger.info("".join(["Статус код ", str(response.status_code)]))
        logger.info(response.json()['detail'])

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
