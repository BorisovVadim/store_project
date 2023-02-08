from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import ProductCategory, Product, Basket

PER_PAGE = 3


class IndexView(TemplateView):
    """CBV для отображения шаблона домашней страницы"""

    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        """Метод возвращает словарь для использования в шаблоне"""
        context = super().get_context_data()
        context['title'] = 'Store'
        return context


# def index(request):
#     context = {'title': 'Store'}
#     return render(request, 'products/index.html', context)


class ProductsListViews(ListView):
    """CBV для отображения шаблона со списком всех доступных продуктов"""

    model = Product
    template_name = 'products/products.html'
    paginate_by = PER_PAGE

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
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context


# def products(request, category_id=None, page_number=1):
#     """
#     Контроллер для отображения всех продуктов или для отображения
#     товаров определенных отфильтрованных по категории продуктов
#     """
#
#     products = Product.objects.filter(
#         category_id=category_id) if category_id else Product.objects.all()
#
#     paginator = Paginator(products, PER_PAGE)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Store - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator
#     }
#     return render(request, 'products/products.html', context)


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
