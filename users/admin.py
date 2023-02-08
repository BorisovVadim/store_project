from django.contrib import admin

from .models import User
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для отображения и работы с пользователем в админке,
    так же позволяет работать с корзинами пользователя, которые
    отображаются в админке пользователя
    """

    list_display = ('username',)
    inlines = (BasketAdmin,)  # Добавляем отображение в админке в User всех
    # корзин, выбранных для пользователя

