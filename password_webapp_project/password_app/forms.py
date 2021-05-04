from django import forms
from django.urls import reverse_lazy

from .models import Password


class PasswordCreateForm(forms.ModelForm):
    expiration_date = forms.DateField(label="Hasło wygasa w dniu", widget=forms.widgets.DateInput(
        format=('%Y-%m-%d'),
        attrs={
            'type': 'date'
        }
    ))

    class Meta:
        model = Password
        exclude = ['password_owner']
        success_url = reverse_lazy('password_app:list')


