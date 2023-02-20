from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    """Класс для тестирования UserRegistrationView"""

    def setUp(self):
        """Метод для создания переменных path и data и дальнейшего обращения к ним"""
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Vadim',
            'last_name': 'Borisov',
            'username': 'malabarsik',
            'email': 'malabarsik2@mail.ru',
            'password1': 'Vad5676755',
            'password2': 'Vad5676755',
        }

    def test_user_registration_get(self):
        """Метод для проверки get-запроса"""
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        """Метод для проверки post-запроса"""
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)  # Передаем данные в post-запрос

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # Проверяем, что код состояния Http 302,
        self.assertRedirects(response, reverse('users:login'))  # Проверяем, что перенаправляет на users/login
        self.assertTrue(User.objects.filter(username=username).exists())

        # Проверяем создание верификации электронной почты
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(email_verification.first().expiration.date(), (now() + timedelta(hours=48)).date())

    def test_user_registration_post_error(self):
        """Метод для проверки вывода ошибки при регистрации,
        если пользователь уже существует
        """

        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
