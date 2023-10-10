from django.contrib import admin

# Register your models here.
from django.contrib import admin

from client.models import MailingSettings, Client, MailingMessage


@admin.register(MailingSettings)
class MailingSettings(admin.ModelAdmin):
    list_display = ('start_time', 'status')


@admin.register(Client)
class Client(admin.ModelAdmin):
    list_display = ('email', 'full_name')
    list_filter = ('email',)


@admin.register(MailingMessage)
class MailingMessage(admin.ModelAdmin):
    list_display = ('subject', 'message')
    list_filter = ('subject',)
