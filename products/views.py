from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import ProductCategory, Product, Basket

PER_PAGE = 3


def index(request):
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):
    """
    Контроллер для отображения всех продуктов или для отображения
    товаров определенных отфильтрованных по категории продуктов
    """

    products = Product.objects.filter(
        category_id=category_id) if category_id else Product.objects.all()

    paginator = Paginator(products, PER_PAGE)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator
    }
    return render(request, 'products/products.html', context)


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
