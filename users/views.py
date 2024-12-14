import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from config.settings import EMAIL_HOST_USER
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from .forms import UserRegisterForm
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView
from .forms import UserForgotPasswordForm, UserRegisterForm, UserSetNewPasswordForm, UserUpdateForm
from .models import CustomUser
from django.http import HttpResponseForbidden


class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

#     def form_valid(self, form):
#         user = form.save()
#         user.is_active = False
#         token = secrets.token_hex(16)
#         user.token = token
#         user.save()
#         host = self.request.get_host()
#         url = f"http://{host}/users/email_confirm/{token}/"
#         send_mail(
#             subject="Активация аккаунта",
#             message=f"Для активации вашего аккаунта перейдите по ссылке: {url}",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email],
#         )
#         return super().form_valid(form)
#
#
# def email_verification(request, token):
#     """Контроллер верификации электронной почты."""
#     user = get_object_or_404(CustomUser, token=token)
#     user.is_active = True
#     user.save()
#
#     return redirect("users:login")

    # Создать страницу с сообщением об отправке письма для подтверждения почты
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        # url = f'http://{host}/users/email-confirm/{token}/'
        url = self.request.build_absolute_uri(reverse_lazy('users:email_verification', args=[token]))

        send_mail(
            subject='Подтверждение почты',
            message=f'Привет. Перейди по ссылке для подтверждения почты {url}.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        # Вывод ошибок формы в консоль для отладки
        print("Форма не валидна:", form.errors)

        # Вы можете также добавить дополнительную логику здесь,
        # например, вернуть сообщение об ошибке пользователю.

        # Возвращаем стандартный ответ для невалидной формы
        return super().form_invalid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy('users:login'))


class UserDetailView(DetailView):
    """Контроллер отображения профиля пользователя."""

    model = CustomUser
    template_name = "user_detail.html"


class UserUpdateView(UpdateView):
    """Контроллер обновления профиля пользователя."""

    model = CustomUser

    form_class = UserUpdateForm
    template_name = "user_form.html"
    success_url = reverse_lazy("mail:main")


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """Контроллер по сбросу пароля по почте."""

    form_class = UserForgotPasswordForm
    template_name = "user_password_reset.html"
    success_url = reverse_lazy("mail:main")
    success_message = "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    subject_template_name = "password_subject_reset_mail.txt"
    email_template_name = "password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Контроллер установки нового пароля."""

    form_class = UserSetNewPasswordForm
    template_name = "user_password_set_new.html"
    success_url = reverse_lazy("mail:main")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


class UsersListView(LoginRequiredMixin, ListView):
    """Контроллер отображения списка пользователей сервиса."""

    model = CustomUser
    template_name = "customuser_list.html"


class BlockUserView(LoginRequiredMixin, View):
    """Контроллер блокировки пользователей сервиса."""

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if not request.user.has_perm("can_block_user"):
            return HttpResponseForbidden("У вас нет прав на это действие.")

        user.is_active = False
        user.save()
        return redirect("users:users_list")


class UnblockUserView(LoginRequiredMixin, View):
    """Контроллер разблокировки пользователей сервиса."""

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if not request.user.has_perm("can_block_user"):
            return HttpResponseForbidden("У вас нет прав на это действие.")

        user.is_active = True
        user.save()
        return redirect("users:users_list")

