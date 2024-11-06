
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

