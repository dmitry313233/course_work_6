import random

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.forms import inlineformset_factory
from pytils.translit import slugify

from blog.models import Blog
from client.forms import ClientForm, MailingSettingsForm, MailingMessageForm
from client.models import Client, MailingSettings, MailingMessage, MailingLog


# Create your views here.


def index(request):
    object_list = MailingSettings.objects.all()
    client_list = Client.objects.all()
    cards = Blog.objects.all()
    random_cards = random.choice(cards)

    context = {
        'mailingSetting_list': object_list,
        'mailingSetting_active': object_list.filter(status=MailingSettings.STATUSES[1][0]),
        'client_list': client_list,
        'random_cards': random_cards,
    }
    return render(request, 'client/page_list.html', context)

class ClientCreateView(CreateView):  # Создаем базу !
    model = Client
    form_class = ClientForm
    template_name = 'client/create_client.html'
    success_url = reverse_lazy('client:home')  # ОН нас сохраняет на главной ЭТОГО НЕ НУЖНО!!!


class ClientListView(ListView):  # Создаем рамку рассылки !
    model = Client
    template_name = 'client/home.html'

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser or user.is_staff:
    #         object_list = Client.objects.all()
    #     else:
    #         object_list = Client.objects.filter(owner=user)
    #     return object_list


class ClientUpdateView(UpdateView):  # Редактирование клиента(в карточке)
    model = Client
    form_class = ClientForm
    template_name = 'client/client_update.html'
    success_url = reverse_lazy('client:home')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/client_detail.html'

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     VersionFormset = inlineformset_factory(Client, MailingMessage, form=MailingSettingsForm, extra=1)  # extra - это сколько форм мы хотим добавить в шаблон
    #     if self.request.method == 'POST':
    #         formset = VersionFormset(self.request.POST, instance=self.object)
    #     else:
    #         formset = VersionFormset(instance=self.object)
    #
    #     context_data['formset'] = formset
    #     return context_data


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client/client_delete.html'
    success_url = reverse_lazy('client:home')




class MailingSettingsCreateView(CreateView):  # Мы создаём рассылку
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'client/create_form.html'
    success_url = reverse_lazy('client:mailingSettings_forms')


class MailingSettingsListView(ListView):
    model = MailingSettings
    template_name = 'client/mailingSettings_forms.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            object_list = MailingSettings.objects.all()
        else:
            object_list = MailingSettings.objects.filter(owner=user)
        return object_list


    def get_object(self, queryset=None):  # "Это для этого ? Не может управлять списком рассылок.
        self.object = super().get_object(queryset)   # Тут мы получаем рассылку mailingSettings_update.html'
        if self.object.owner != self.request.user and not self.request.user.is_superuser:   # "Это строка для менеджера
            raise Http404
        return self.object


    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser or user.is_staff:
    #         object_list = Client.objects.all()
    #     else:
    #         object_list = Client.objects.filter(owner=user)
    #     return object_list


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'client/mailingSettings_update.html'
    success_url = reverse_lazy('client:mailingSettings_forms')

    def get_object(self, queryset=None):  # ЭТО ПИШЕСТЯ ДЛЯ ТOГО ЧТОБЫ МЕНЕДЖЕР НЕ МОГ РЕДАКТИРОВАТЬ РАССЫЛКИ
        self.object = super().get_object(queryset)   # Тут мы получаем рассылку mailingSettings_update.html'
        if self.object.owner != self.request.user and not self.request.user.is_superuser:   # Это строка для менеджера
            raise Http404
        return self.object

class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    template_name = 'client/mailingSettings_delete.html'
    success_url = reverse_lazy('client:mailingSettings_forms')





class MailingMessageCreateView(CreateView):  # Создание сообщения работает
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'client/mailing_message_create.html'
    success_url = reverse_lazy('client:mailinmessage_form')


class MailingMessageListView(ListView):   # Отображение сообщений работает
    model = MailingMessage
    template_name = 'client/mailinmessage_form.html'

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser or user.is_staff:
    #         object_list = Client.objects.all()
    #     else:
    #         object_list = Client.objects.filter(owner=user)
    #     return object_list


class MailingMessageUpdateView(UpdateView):  # Редактирование сообщения работает
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'client/mailin_message_update.html'
    success_url = reverse_lazy('client:mailinmessage_form')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)   # Тут мы получаем рассылку mailingSettings_update.html'
        if self.object.owner != self.request.user and not self.request.user.is_superuser:   # Это строка для менеджера
            raise Http404
        return self.object




class MailingMessageDeleteView(DeleteView):  # Удаление сообщения работает
    model = MailingMessage
    template_name = 'client/mailing_message_delete.html'
    success_url = reverse_lazy('client:mailinmessage_form')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)   # Тут мы получаем рассылку mailingSettings_update.html'
        if self.object.owner != self.request.user and not self.request.user.is_superuser:   # "Это строка для менеджера
            raise Http404
        return self.object




def switch_status_newsletter(request, pk):
    """Контроллер для смены статуса рассылки"""
    mailing = MailingSettings.objects.get(pk=pk)
    if mailing.status == 'Создана':
        mailing.status = 'Завершена'
    elif mailing.status == 'Завершена':
        mailing.status = 'Создана'
    mailing.save()
    return redirect('client:mailingSettings_forms')