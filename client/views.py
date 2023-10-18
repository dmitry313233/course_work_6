import random

from django.contrib.auth.mixins import LoginRequiredMixin
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



class IsNotManagerMixin:
    def get_object(self, queryset=None):  # ЭТО ПИШЕСТЯ ДЛЯ ТOГО ЧТОБЫ МЕНЕДЖЕР НЕ МОГ РЕДАКТИРОВАТЬ РАССЫЛКИ(один объект)
        self.object = super().get_object(queryset)   # Тут мы получаем рассылку mailingSettings_update.html'
        user = self.request.user
        if self.object.owner != user and not user.is_superuser:   # Это строка для менеджера
            raise Http404
        return self.object


def index(request):
    object_list = MailingSettings.objects.all()
    client_list = Client.objects.all()

    context = {
        'mailingSetting_list': object_list,
        'mailingSetting_active': object_list.filter(status=MailingSettings.STATUSES[1][0]),
        'client_list': client_list,
    }
    return render(request, 'client/page_list.html', context)

class ClientCreateView(LoginRequiredMixin, CreateView):  # LoginRequiredMixin запрещает не зарегистрированным пользователям делать действия
    model = Client
    form_class = ClientForm
    template_name = 'client/create_client.html'
    success_url = reverse_lazy('client:home')  # ОН нас сохраняет на главной ЭТОГО НЕ НУЖНО!!!

    def form_valid(self, form):  # Этот метод
        user = self.request.user  # считывает зарегистрированные данные пользователя
        self.object = form.save()
        self.object.owner = user
        self.object.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):  # Создаем рамку рассылки !
    model = Client
    template_name = 'client/home.html'

    def get_queryset(self):   # Берем из бызы данных
        user = self.request.user
        if user.is_superuser or user.is_staff:
            object_list = Client.objects.all()
        else:
            object_list = Client.objects.filter(owner=user)
        return object_list


class ClientUpdateView(LoginRequiredMixin, UpdateView):  # Редактирование клиента(в карточке)
    model = Client
    form_class = ClientForm
    template_name = 'client/client_update.html'
    success_url = reverse_lazy('client:home')


class ClientDetailView(LoginRequiredMixin, DetailView):
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


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/client_delete.html'
    success_url = reverse_lazy('client:home')




class MailingSettingsCreateView(LoginRequiredMixin, CreateView):  # Мы создаём рассылку
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'client/create_form.html'
    success_url = reverse_lazy('client:mailingSettings_forms')

    def get_form_kwargs(self, form_class=None):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):  # Этот метод
        user = self.request.user  # считывает зарегистрированные данные пользователя
        self.object = form.save()
        self.object.owner = user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'client/mailingSettings_forms.html'

    def get_queryset(self):   # Берем из базы данных
        user = self.request.user
        if user.is_superuser or user.is_staff:
            object_list = MailingSettings.objects.all()
        else:
            object_list = MailingSettings.objects.filter(owner=user)
        return object_list


    def get_object(self, queryset=None):  #Не может управлять списком рассылок.
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


class MailingSettingsUpdateView(LoginRequiredMixin, IsNotManagerMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'client/mailingSettings_update.html'
    success_url = reverse_lazy('client:mailingSettings_forms')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    template_name = 'client/mailingSettings_delete.html'
    success_url = reverse_lazy('client:mailingSettings_forms')





class MailingMessageCreateView(LoginRequiredMixin, CreateView):  # Создание сообщения работает
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'client/mailing_message_create.html'
    success_url = reverse_lazy('client:mailinmessage_form')

    def form_valid(self, form):  # Этот метод
        user = self.request.user  # считывает зарегистрированные данные пользователя
        self.object = form.save()
        self.object.owner = user
        self.object.save()
        return super().form_valid(form)


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


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):  # Редактирование сообщения работает
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'client/mailin_message_update.html'
    success_url = reverse_lazy('client:mailinmessage_form')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)   # Тут мы получаем рассылку mailingSettings_update.html'
        if self.object.owner != self.request.user and not self.request.user.is_superuser:   # Это строка для менеджера
            raise Http404
        return self.object




class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):  # Удаление сообщения работает
    model = MailingMessage
    template_name = 'client/mailing_message_delete.html'
    success_url = reverse_lazy('client:mailinmessage_form')

    def get_object(self, queryset=None):  # Пишем для того чтобы другой пользователь не мог удалить наше сообщение
        self.object = super().get_object(queryset)   # Тут мы получаем рассылку mailing_message_delete.html
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