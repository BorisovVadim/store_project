from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            # данное сообщение можно передавать в шаблоны login и registration
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    """
    Контроллер отображает шаблон с заполненной данными пользователя формой и
    обновляет информацию о пользователе в ней, если нужно.
    """

    if request.method == 'POST':
        form = UserProfileForm(
            instance=request.user,  # берем уже существующего пользователя
            data=request.POST,  # и обновляем его данные
            files=request.FILES  # необходимо для работы с изображениями
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)  # Заполняем форму
        # данными существующего пользователя

    baskets = Basket.objects.filter(user=request.user)  # Присваиваем QuerySet
    # Basket для работы в шаблонах profile.html и baskets.html, отфильтрованную
    # по пользователю, чтобы показывались только продукты, добавленные
    # пользователем в корзину
    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': baskets,
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    """
    Контроллер для выхода пользователя из системы.
    Возвращает пользователя на главную страницу.
    """

    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
