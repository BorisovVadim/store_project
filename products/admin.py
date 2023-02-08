from django.contrib import admin

from .models import ProductCategory, Product, Basket

admin.site.register(ProductCategory)


@admin.register(Product)  # указываем с какой моделью будет работать класс
class ProductAdmin(admin.ModelAdmin):
    """Класс для оформления отображения
    информации о модели Product в админке
    """

    list_display = ('name', 'price', 'quantity', 'category')
    fields = (
        'name', 'description', ('price', 'quantity'), 'image', 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    """Класс для отображения всех корзин с
    продуктами для пользователя в админке User,
    является частью админки User
    """

    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0  # чтобы не было пустых строчек с продуктами в инлайне

