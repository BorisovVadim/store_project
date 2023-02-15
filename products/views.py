from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin

from .models import Basket, Product, ProductCategory

PER_PAGE = 3


class IndexView(TitleMixin, TemplateView):
    """CBV для отображения шаблона домашней страницы"""

    template_name = 'products/index.html'
    title = 'Store'  # Присваиваем переменной TitleMixin.title значение


class ProductsListViews(TitleMixin, ListView):
    """CBV для отображения шаблона со списком всех доступных продуктов"""

    model = Product
    template_name = 'products/products.html'
    paginate_by = PER_PAGE
    title = 'Store - Каталог'

    def get_queryset(self):
        """Переопределяем метод. Если category_id == None, возвращает
        весь queryset; если category_id != None, возвращает queryset
        продуктов, отфильтрованных по переданной категории
        """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')  # Достаем category_id из
        # словаря со всеми данными. Если category_id нет, get() вернет None
        if category_id:
            return queryset.filter(category_id=category_id)
        else:
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    """Контроллер для добавления продуктов в корзину."""

    product = Product.objects.get(id=product_id)  # Присваиваем переменной
    # product продукт по id из таблицы Product
    baskets = Basket.objects.filter(user=request.user, product=product)
    # Берем все элементы корзины, которые принадлежат пользователю из запроса,
    # и все продукты

    if not baskets.exists():  # Если QuarrySet корзины пустой:
        Basket.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )  # создаем ее
    else:  # Если продукт уже есть в корзине:
        basket = baskets.first()
        basket.quantity += 1  # увеличиваем количество продуктов на 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # Возвращаем
    # пользователя на ту страницу, с которой он добавлял продукт в корзину


@login_required
def basket_remove(request, basket_id):
    """Контроллер для удаления продуктов с корзины"""

    basket = Basket.objects.get(id=basket_id)  # Присваиваем переменной
    # basket продукт в корзине по id
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
