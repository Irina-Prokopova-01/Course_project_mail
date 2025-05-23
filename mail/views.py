from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Mailing, Attempts, Message, Recipient
from .forms import RecipientForm, MailingForm, MessageForm
from .service import get_mailing_attempts_list, get_mailing_list, get_message_list, get_recipient_list


class MailingView(TemplateView):
    """Контроллер отображения главной страницы с рассылками."""
    models = [Recipient, Mailing]
    template_name = "mail/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipients_all"] = Recipient.objects.all()
        context["mailing_all"] = Mailing.objects.all()
        context["mailing_active"] = Mailing.objects.filter(status=Mailing.ACTIVE)
        return context


class RecipientListView(LoginRequiredMixin, ListView):
    """Контроллер отображения списка получателей."""
    model = Recipient
    template_name = "mail/recipient_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_recipient"):
            return get_recipient_list()
        return get_recipient_list().filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения подробностей о получателе."""
    model = Recipient
    template_name = "mail/recipient_detail.html"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания получателя."""
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")

    def form_valid(self, form):
        recipients = form.save()
        user = self.request.user
        recipients.owner = user
        recipients.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер изменения получателя."""
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.owner

    def handle_no_permissions(self):
        return HttpResponseForbidden("У вас нет прав на это действие.")

    def get_success_url(self):
        return reverse_lazy("mail:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    template_name = "mail/recipient_confirm_delete.html"
    success_url = reverse_lazy("mail:recipient_list")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.owner

    def handle_no_permissions(self):
        return HttpResponseForbidden("У вас нет прав на это действие.")


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер отображения списка сообщений."""
    model = Message
    template_name = "mail/message_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_message"):
            return get_message_list()
        return get_message_list().filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения подробностей о сообщении."""
    model = Message
    template_name = "mail/message_detail.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания сообщения."""
    model = Message
    form_class = MessageForm
    template_name = "mail/message_form.html"
    success_url = reverse_lazy("mail:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер изменения сообщения."""
    model = Message
    form_class = MessageForm
    template_name = "mail/message_form.html"
    success_url = reverse_lazy("mail:message_list")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.owner

    def handle_no_permissions(self):
        return HttpResponseForbidden("У вас нет прав на это действие.")

    def get_success_url(self):
        return reverse_lazy("mail:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления сообщения."""
    model = Message
    template_name = "mail/message_confirm_delete.html"
    success_url = reverse_lazy("mail:message_list")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.owner

    def handle_no_permissions(self):
        return HttpResponseForbidden("У вас нет прав на это действие.")


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер отображения списка рассылок."""
    model = Mailing
    template_name = "mail/mailing_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_mailing"):
            return get_mailing_list()
        return get_mailing_list().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_queryset()
        context["mailing_created"] = mailing.filter(status=Mailing.CREATED)
        context["mailing_active"] = mailing.filter(status=Mailing.ACTIVE)
        context["mailing_finished"] = mailing.filter(status=Mailing.FINISHED)
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения подробностей о рассылке."""
    model = Mailing
    template_name = "mail/mailing_detail.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер изменения рассылки."""
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.owner

    def handle_no_permissions(self):
        return HttpResponseForbidden("У вас нет прав на это действие.")

    def get_success_url(self):
        return reverse_lazy("mail:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления рассылки."""
    model = Mailing
    template_name = "mail/mailing_confirm_delete.html"
    success_url = reverse_lazy("mail:mailing_list")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.owner

    def handle_no_permissions(self):
        return HttpResponseForbidden("У вас нет прав на это действие.")


class AttemptsListView(LoginRequiredMixin, ListView):
    """Контроллер отображения списка попыток отправки."""
    model = Attempts
    template_name = "mail/mailing_attempts_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_mailing_attempts"):
            return get_mailing_attempts_list()
        return get_mailing_attempts_list().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt = self.get_queryset()
        context["success"] = attempt.filter(attempt_status="успешно").count()
        context["failure"] = attempt.filter(attempt_status="неуспешно").count()
        context["total"] = attempt.count()
        return context


def sending_mail(request, pk):
    """Контроллер отправки рассылок. Принимает pk рассылки,
    отправляет согласно списка рассылки, вносит необходимые данные в БД"""
    mail = Mailing.objects.get(pk=pk)
    email_from = settings.EMAIL_HOST_USER
    attempts_list = []
    subject = mail.message.subject
    message = mail.message.text
    owner = mail.owner
    recipients_list = [recipient.email for recipient in mail.recipients.all()]
    for recipient in recipients_list:
        try:
            send_mail(subject, message, email_from, recipient_list=[recipient])
            if mail.status == Mailing.CREATED:
                mail.status = Mailing.ACTIVE
                mail.start_at = datetime.now()
                mail.save()
            mailing_attempts = Attempts(
                attempt_date=datetime.now(),
                attempt_status=Attempts.SUCCESS,
                mail_server_response="Email sent successfully",
                mailing=mail,
                owner=owner,
            )
            mailing_attempts.save()
            result = "Sending mail successful"
            attempts_list.append((result, subject, message, recipient))
        except Exception as e:
            if mail.status == Mailing.CREATED:
                mail.status = Mailing.ACTIVE
                mail.start_at = datetime.now()
                mail.save()
            mailing_attempts = Attempts(
                attempt_date=datetime.now(),
                attempt_status=Attempts.FAILURE,
                mail_server_response=str(e),
                mailing=mail,
                owner=owner,
            )
            mailing_attempts.save()
            result = f"Sending mail failed with: {str(e)}"
            attempts_list.append((result, subject, message, recipient))
    context = {"attempts_list": attempts_list}
    return render(request, "mail/send_mail_result.html", context)


def finish_mailing(request, pk):
    """Контроллер завершения рассылки. Принимает pk рассылки,
    помечает рассылку как завершенную, вносит необходимые данные в БД"""
    mail = Mailing.objects.get(pk=pk)
    mail.status = Mailing.FINISHED
    mail.end_at = datetime.now()
    mail.save()
    context = {"mail": mail}
    return render(request, "mail/finished_mailing_info.html", context)