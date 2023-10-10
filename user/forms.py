from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from client.forms import StyleFormMixin
from user.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
