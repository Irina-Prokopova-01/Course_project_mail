from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Mailing, Attempts, Message, Recipient
from .forms import RecipientForm, MailingForm, MessageForm


class MailingView(TemplateView):
    models = [Recipient, Mailing]
    template_name = "mail/main.html"


class RecipientListView(ListView):
    model = Recipient
    template_name = "mail/recipient_list.html"


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "mail/recipient_detail.html"


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")

    def get_success_url(self):
        return reverse_lazy("mail:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "mail/recipient_confirm_delete.html"
    success_url = reverse_lazy("mail:recipient_list")


class MessageListView(ListView):
    model = Message
    template_name = "mail/message_list.html"


class MessageDetailView(DetailView):
    model = Message
    template_name = "mail/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mail/message_form.html"
    success_url = reverse_lazy("mail:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mail/message_form.html"
    success_url = reverse_lazy("mail:message_list")

    def get_success_url(self):
        return reverse_lazy("mail:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mail/message_confirm_delete.html"
    success_url = reverse_lazy("mail:message_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "mail/mailing_list.html"


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mail/mailing_detail.html"


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")

    def get_success_url(self):
        return reverse_lazy("mail:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mail/mailing_confirm_delete.html"
    success_url = reverse_lazy("mail:mailing_list")


class AttemptsListView(ListView):
    model = Attempts
    template_name = "mail/mailing_attempts_list.html"


def sending_mail_active(request, *args, **kwargs):
    mails = Mailing.objects.filter(status=Mailing.ACTIVE)
    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    for mailing in mails:
        subject = mailing.message.subject
        message = mailing.message.text
        recipient_list = [recipient.email for recipient in mailing.recipients.all()]

        try:
            send_mail(subject, message, email_from, recipient_list)
            mailing_attempts = Attempts(
                attempt_date=datetime.now(),
                attempt_status=Attempts.SUCCESS,
                mail_server_response="Email sent successfully",
                mailing=mailing,
            )
            mailing_attempts.save()
            result = "Sending mail successful"

            attempts_list.append((result, subject, message, recipient_list))

        except Exception as e:
            mailing_attempts = Attempts(
                attempt_date=datetime.now(),
                attempt_status=Attempts.FAILURE,
                mail_server_response=str(e),
                mailing=mailing,
            )
            mailing_attempts.save()
            result = f"Sending mail failed with: {str(e)}"

            attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mail/send_mail_result.html", context)


def sending_one_mail_active(request, pk):
    mail = Mailing.objects.get(pk=pk)

    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    subject = mail.message.subject
    message = mail.message.text
    recipient_list = [recipient.email for recipient in mail.recipients.all()]

    try:
        send_mail(subject, message, email_from, recipient_list)
        mailing_attempts = Attempts(
            attempt_date=datetime.now(),
            attempt_status=Attempts.SUCCESS,
            mail_server_response="Email sent successfully",
            mailing=mail,
        )
        mailing_attempts.save()
        result = "Sending mail successful"

        attempts_list.append((result, subject, message, recipient_list))

    except Exception as e:
        mailing_attempts = Attempts(
            attempt_date=datetime.now(),
            attempt_status=Attempts.FAILURE,
            mail_server_response=str(e),
            mailing=mail,
        )
        mailing_attempts.save()
        result = f"Sending mail failed with: {str(e)}"

        attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mail/send_mail_result.html", context)


def sending_mail_created(request, *args, **kwargs):
    mails = Mailing.objects.filter(status=Mailing.CREATED)
    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    for mailing in mails:
        subject = mailing.message.subject
        message = mailing.message.text
        recipient_list = [recipient.email for recipient in mailing.recipients.all()]

        try:
            send_mail(subject, message, email_from, recipient_list)
            mailing.status = Mailing.ACTIVE
            mailing.start_at = datetime.now()
            mailing.save()
            mailing_attempts = Attempts(
                attempt_date=datetime.now(),
                attempt_status=Attempts.SUCCESS,
                mail_server_response="Email sent successfully",
                mailing=mailing,
            )
            mailing_attempts.save()
            result = "Sending mail successful"
            attempts_list.append((result, subject, message, recipient_list))

        except Exception as e:
            mailing.status = Mailing.ACTIVE
            mailing.start_at = datetime.now()
            mailing.save()
            mailing_attempts = Attempts(
                attempt_date=datetime.now(),
                attempt_status=Attempts.FAILURE,
                mail_server_response=str(e),
                mailing=mailing,
            )
            mailing_attempts.save()
            result = f"Sending mail failed with: {str(e)}"
            attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mail/send_mail_result.html", context)


def sending_one_mail_created(request, pk):
    mail = Mailing.objects.get(pk=pk)

    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    subject = mail.message.subject
    message = mail.message.text
    recipient_list = [recipient.email for recipient in mail.recipients.all()]

    try:
        send_mail(subject, message, email_from, recipient_list)
        mail.status = Mailing.ACTIVE
        mail.start_at = datetime.now()
        mail.save()
        mailing_attempts = Attempts(
            attempt_date=datetime.now(),
            attempt_status=Attempts.SUCCESS,
            mail_server_response="Email sent successfully",
            mailing=mail,
        )
        mailing_attempts.save()
        result = "Sending mail successful"
        attempts_list.append((result, subject, message, recipient_list))

    except Exception as e:
        mail.status = Mailing.ACTIVE
        mail.start_at = datetime.now()
        mail.save()
        mailing_attempts = Attempts(
            attempt_date=datetime.now(),
            attempt_status=Attempts.FAILURE,
            mail_server_response=str(e),
            mailing=mail,
        )
        mailing_attempts.save()
        result = f"Sending mail failed with: {str(e)}"
        attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mail/send_mail_result.html", context)


def finish_mailing(request, pk):
    mail = Mailing.objects.get(pk=pk)
    mail.status = Mailing.FINISHED
    mail.end_at = datetime.now()
    mail.save()
    context = {"mail": mail}
    return render(request, "mail/mailing_info.html", context)
