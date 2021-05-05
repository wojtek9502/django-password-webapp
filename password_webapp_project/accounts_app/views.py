from django.urls import reverse_lazy
from django.views import generic

from .forms import UserCreateForm


class AfterLogoutView(generic.TemplateView):
    template_name = "accounts_app/after_logout.html"


class RegisterView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts_app:login')
    template_name = 'accounts_app/register.html'


class AccountSettingsView(generic.TemplateView):
    template_name = "accounts_app/account_settings.html"
