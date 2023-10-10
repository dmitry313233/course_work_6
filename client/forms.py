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
        fields = '__all__'


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        # fields = ('start_time', 'end_time', 'period')
        fields = '__all__'


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
        fields = '__all__'
#
#
# class MailingLogForm(forms.ModelForm):
#     class Meta:
#         model = MailingLog
#         fields = ('last_try', 'status')
