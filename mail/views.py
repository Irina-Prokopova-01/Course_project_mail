from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Mailing, Attempts, Message, Recipient


class MailingView(TemplateView):
    models = [Recipient, Mailing]
    template_name = "mail/main.html"


class RecipientListView(ListView):
    model = Recipient
    template_name = "mail/recipient_list.html"
