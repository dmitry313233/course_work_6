from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import ClientDetailView, ClientDeleteView, \
    MailingSettingsCreateView, MailingMessageCreateView, ClientCreateView, ClientUpdateView, ClientListView, \
    MailingMessageListView, MailingMessageUpdateView, MailingMessageDeleteView, MailingSettingsListView, \
    MailingSettingsUpdateView, MailingSettingsDeleteView, switch_status_newsletter, index

app_name = ClientConfig.name



urlpatterns = [
    path('', ClientListView.as_view(), name='home'),
    path('page_list/', index, name='page_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_detail/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('create_form/', MailingSettingsCreateView.as_view(), name='create_form'),  # Создает рассылку
    path('mailingSettings_forms/', MailingSettingsListView.as_view(), name='mailingSettings_forms'),
    path('mailingSettings_update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='mailingSettings_update'),
    path('mailingSettings_delete.html/<int:pk>/', cache_page(60)(MailingSettingsDeleteView.as_view()), name='mailingSettings_delete'),

    path('mailing_message_create/', MailingMessageCreateView.as_view(), name='mailing_message_create'),
    path('mailinmessage_form/', MailingMessageListView.as_view(), name='mailinmessage_form'),
    path('mailin_message_update/<int:pk>/', MailingMessageUpdateView.as_view(), name='mailin_message_update'),
    path('mailing_message_delete/<int:pk>/', cache_page(60)(MailingMessageDeleteView.as_view()), name='mailing_message_delete'),

    path('switch_status_newsletter/<int:pk>/', switch_status_newsletter, name='switch_status_newsletter'),

]
