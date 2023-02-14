from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail


class User(AbstractUser):
    """Модель для пользователя"""

    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)  # Подтвердил ли
    # пользователь свою почту


class EmailVerification(models.Model):
    """Модель для подтверждения почты пользователя"""

    code = models.UUIDField(unique=True)  # Формирует уникальный код для юзера
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()  # Срок действия ссылки

    def __str__(self) -> str:
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        """Метод отправляет электронное письмо пользователю для верификации"""
        send_mail(
            'Subject here',
            'Test verification email.',
            'from@example.com',
            [self.user.email],
            fail_silently=False,
        )
