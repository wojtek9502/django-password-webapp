from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')
        model = get_user_model()


class UserEmailChangeForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=1000, required=True)


class UserPasswordChangeForm(forms.Form):
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(), max_length=1000, required=True)
    password2 = forms.CharField(label="Hasło raz jeszcze", widget=forms.PasswordInput(), max_length=1000, required=True)

    def clean(self):
        cleaned_data = super(UserPasswordChangeForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self._errors['password2'] = self.error_class(['Hasła muszą być takie same.'])
            del self.cleaned_data['password2']
        return cleaned_data