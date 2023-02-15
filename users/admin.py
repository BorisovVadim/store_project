from django.contrib import admin

from products.admin import BasketAdmin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для отображения и работы с пользователем в админке,
    так же позволяет работать с корзинами пользователя, которые
    отображаются в админке пользователя
    """

    list_display = ('username',)
    inlines = (BasketAdmin,)  # Добавляем отображение в админке в User всех
    # корзин, выбранных для пользователя


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """Класс для отображения верификации почты пользователя в админке"""
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
