from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from client.forms import StyleFormMixin
from user.models import User
from django import forms


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()