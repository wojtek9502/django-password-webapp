from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy

from .models import Password



class PasswordCreateForm(forms.ModelForm):
    class Meta:
        model = Password
        exclude = ['password_owner']
        success_url = reverse_lazy('password_app:list')
