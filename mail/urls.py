from django.urls import path
from django.views.decorators.cache import cache_page

from mail.apps import MailConfig
from mail.views import MailingView, RecipientDetailView, RecipientCreateView, RecipientDeleteView, RecipientUpdateView, RecipientListView, MessageListView, MessageCreateView, MessageDeleteView, MailingDetailView, MessageUpdateView, MailingCreateView, MailingDeleteView, MailingUpdateView, MailingListView, MessageDetailView, AttemptsListView, finish_mailing, sending_mail

app_name = MailConfig.name

urlpatterns = [
    path("", MailingView.as_view(), name="main"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("messages/", cache_page(60)(MessageListView.as_view()), name="message_list"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/", cache_page(60)(MailingListView.as_view()), name="mailing_list"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing_attempts/", AttemptsListView.as_view(), name="mailing_attempts_list"),
    path("finish_mailing/<int:pk>/", finish_mailing, name="finish_mailing"),
    path("send_mail/<int:pk>/", sending_mail, name="send_mail"),

]