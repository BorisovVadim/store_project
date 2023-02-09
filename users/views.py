from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
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


class UserRegistrationView(CreateView):
    """CBV для регистрации пользователя. Если регистрация прошла
    успешно - перенаправляет пользователя на страницу логина
    """

    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - Регистрация'
        return context


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрированы!')
#             # данное сообщение можно передавать в шаблоны login и registration
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        """Переопределяем метод, передаем id объекта User"""
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.object)
        # self.object альтернатива self.request.user
        return context


# @login_required
# def profile(request):
#     """
#     Контроллер отображает шаблон с заполненной данными пользователя формой и
#     обновляет информацию о пользователе в ней, если нужно.
#     """
#
#     if request.method == 'POST':
#         form = UserProfileForm(
#             instance=request.user,  # берем уже существующего пользователя
#             data=request.POST,  # и обновляем его данные
#             files=request.FILES  # необходимо для работы с изображениями
#         )
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)  # Заполняем форму
#         # данными существующего пользователя
#
#     baskets = Basket.objects.filter(user=request.user)  # Присваиваем QuerySet
#     # Basket для работы в шаблонах profile.html и baskets.html, отфильтрованную
#     # по пользователю, чтобы показывались только продукты, добавленные
#     # пользователем в корзину
#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         'baskets': baskets,
#     }
#     return render(request, 'users/profile.html', context)


def logout(request):
    """
    Контроллер для выхода пользователя из системы.
    Возвращает пользователя на главную страницу.
    """

    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
