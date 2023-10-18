from django import forms

from client.models import Client, MailingSettings, MailingMessage, MailingLog


class StyleFormMixin:  # Это для добавления стилей в колонке
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):

    clients = forms.ModelChoiceField(
        label='Clients',
        queryset=Client.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'})
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['clients'].queryset = Client.objects.all()
        elif user:
            self.fields['clients'].queryset = Client.objects.filter(owner=user)
        else:
            self.fields['clients'].queryset = Client.objects.none()

    class Meta:
        model = MailingSettings
        # fields = ('start_time', 'end_time', 'period')
        exclude = ('owner',)


#
# class MailingClientForm(forms.ModelForm):
#     class Meta:
#         model = MailingClient
#         fields = '__all__'
#
#
class MailingMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        exclude = ('owner',)
#
#
# class MailingLogForm(forms.ModelForm):
#     class Meta:
#         model = MailingLog
#         fields = ('last_try', 'status')
