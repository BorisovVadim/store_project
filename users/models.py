from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


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
        """Метод формирует ссылку для верификации
        пользователя и отправляет письмо на электронную почту
        пользователя для верификации аккаунта
        """
        link = reverse('users:email_verification',
                       kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = (f'Для подтверждения учетной записи для {self.user.email} '
                   f'перейдите по ссылке: {verification_link}')
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        """Метод возвращает True, если ссылка для
        подтверждения учетной записи все еще активна
        """
        return True if now() >= self.expiration else False
