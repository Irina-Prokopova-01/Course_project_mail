import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
from .forms import UserRegisterForm


class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    # Создать страницу с сообщением об отправке письма для подтверждения почты
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            subject="Активация аккаунта",
            message=f"Для активации вашего аккаунта перейдите по ссылке: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()

    return redirect(reverse('users:login'))

