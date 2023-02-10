from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from products.models import Basket


class UserLoginView(LoginView):
    """CBV для логина пользователя. Используется
    модель User, прописанная в settings.py
    """

    template_name = 'users/login.html'
    form_class = UserLoginForm


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
