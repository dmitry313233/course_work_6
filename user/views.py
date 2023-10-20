from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse

from config import settings
from user.forms import UserRegisterForm, UserForm
from user.models import User
import random

# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('client:home')

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            cod = ''.join([str(random.randint(1, 10)) for i in range(5)])  # это ссылка, высылается по почте
            instance.cod = cod
            url = reverse('user:verification', args=[cod])
            total_url = self.request.build_absolute_uri(url)
            send_mail(
                subject='Успешная верификация',
                message=f'Пройдите по ссылке для успешной верификации: {total_url}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email]
            )
            instance.save()
            return super().form_valid(form)


def verify(request, cod):  # Это контролер на FBV
    user = User.objects.get(cod=cod)
    user.is_active = True
    user.save()
    return redirect(reverse('user:login'))


def switch_status_user(request, pk):
    """Контроллер для смены статуса пользователя"""
    user = User.objects.get(pk=pk)
    user.is_active = not user.is_active
    # if user.is_active:
    #     user.is_active = False
    # else:
    #     user.is_active = True
    user.save()
    return redirect('user:user_list')


class UserListView(ListView):
    model = User


class UserCreateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/profile.html'

    def get_object(self, queryset=None):  # Пишем для получения pk пользователя
        return self.request.user
