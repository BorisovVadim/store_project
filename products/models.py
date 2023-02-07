from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        """Изменяет название модели в админке"""

        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        """Изменяет название модели в админке"""

        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'


class BasketQuerySet(models.QuerySet):
    """Создаем дополнительный менеджер, чтобы
    добавить методы в него total_sum и total_quantity
    """

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)  # Поле всегда
    # заполняется автоматически при создании нового объекта, если переменной
    # auto_now_add присвоено значение True
    objects = BasketQuerySet.as_manager()  # Подключаем дополнительный менеджер

    def __str__(self) -> str:
        return (f'Корзина для {self.user.username} | '
                f'Продукт: {self.product.name}')

    def sum(self):
        return self.product.price * self.quantity
