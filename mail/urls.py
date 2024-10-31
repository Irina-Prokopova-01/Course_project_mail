from django.urls import path

from mail.apps import MailConfig
from mail.views import MailingView, RecipientListView

app_name = MailConfig.name

urlpatterns = [
    path("", MailingView.as_view(), name="main"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
]