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

        response = self.client.post('/accounts/registration', data)

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise User.DoesNotExist("Такого пользователя не существует")

        logger.info("Регистрация пользователя: " + response.json()['message'])
        logger.info(f"Статус код {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.OK,
                         "Успешный запрос на регистрацию пользователя")
        self.assertIsInstance(user, User, "Такой пользователь зарегистрирован")

    def test_registration_user_fail(self):
        data = {
            'username': 'testuserfail',
            "email": 'testemailyandex',
            'password': 'test12345',
            "password2": 'test12345'
        }

        response = self.client.post('/accounts/registration', data)

        logger.info("Ошибка при регистрации пользователя: " + "".join(response.json()['email']))
        logger.info(f"Статус код {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST,
                         "Запрос на регистрацию пользователя с "
                         "неверным email успешно не прошел")

        data['username'] = 'soo'
        data['email'] = 'testemail@yandex.ru'

        response = self.client.post('/accounts/registration', data)

        logger.info("Ошибка при регистрации пользователя: " + response.json()['username'][0])
        logger.info(f"Статус код {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST,
                         "Запрос на регистрацию пользователя с "
                         "неверной длинной username успешно не прошел")

        data['username'] = 'testuserfail'
        data['password'] = '123'
        data['password2'] = '123'

        response = self.client.post('/accounts/registration', data)

        logger.info("Ошибка при регистрации пользователя: " + "".join(response.json()['password2']))
        logger.info(f"Статус код {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST,
                         "Запрос на регистрацию пользователя с "
                         "неверным форматом пароля успешно не прошел")

        data['password'] = '!asdfg123'
        data['password2'] = '!asdfg12'

        response = self.client.post('/accounts/registration', data)

        logger.info("Ошибка при регистрации пользователя: " + response.json()['non_field_errors'][0])
        logger.info(f"Статус код {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST,
                         "Запрос на регистрацию пользователя с "
                         "разными значениями пароль и повторите пароль"
                         "успешно не прошел")

    def test_сustom_auth_token_success(self):
        data = {
            'username': 'testuser',
            'password': 'test123',
        }

        User.objects.create_user(**data)
        response = self.client.post('/accounts/api-token-auth', data)
        token = response.json()['token']

        logger.info(f"Статус код на получение токена пользователем {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.OK,
                         "Запрос на получение токена пользователем успешно прошел")
        self.assertIsNotNone(token, "Токен пользователя не пустой")

    def test_сustom_auth_token_fail(self):
        data = {
            'username': 'testuser1',
            'password': 'test123',
        }

        response = self.client.post('/accounts/api-token-auth', data)

        logger.info("Неправильные введены данные пользователя: " + response.json()['non_field_errors'][0])
        logger.info(f"Статус код на получение токена пользователем {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST,
                         "Запрос на получение токена пользователем который "
                         "не зарегистрирован успешно не прошел")

    def test_authorization_success(self):
        data = {
            'username': 'testuser1',
            'password': 'test123',
        }

        User.objects.create_user(**data)
        token = self.client.post('/accounts/api-token-auth', data, follow=True).json()['token']
        response = self.client.get('/accounts/authentication',
                                   HTTP_AUTHORIZATION="".join(["Token ", token]),
                                   follow=True)
        username = response.json()['username']

        logger.info(f"Статус код при авторизации пользователем {response.status_code}")

        self.assertEqual(username, data['username'], "Профиль пользователя с таким логином существует")
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         "Авторизация пользователя прошла успешно")

    def test_authorization_fail(self):
        response = self.client.get('/accounts/authentication',
                                   HTTP_AUTHORIZATION="Token ",
                                   follow=True)

        logger.info("Данные пользователя введены неправильно: " + response.json()['detail'])
        logger.info(f"Статус код при авторизации пользователем {response.status_code}")

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED,
                         "Не аутентифицированный пользователь не смог войти в профиль")
