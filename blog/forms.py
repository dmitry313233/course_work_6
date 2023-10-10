from blog.models import Blog
from client.forms import StyleFormMixin
from django import forms


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
