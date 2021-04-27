from django import forms
from django.urls import reverse_lazy

from .models import Password


class PasswordCreateForm(forms.ModelForm):
    # password = forms.CharField(label="Hasło", initial="sfadas", max_length=1000,
    #                            widget=forms.PasswordInput(render_value=True) # True means, populate field in template
    #                            )
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
