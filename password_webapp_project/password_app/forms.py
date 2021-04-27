from django import forms
from django.urls import reverse_lazy

from .models import Password


class PasswordCreateForm(forms.ModelForm):
    class Meta:
        model = Password
        exclude = ['password_owner']
        success_url = reverse_lazy('password_app:list')
