from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *


class AfterLogoutView(generic.TemplateView):
    template_name = "accounts_app/after_logout.html"


class RegisterView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts_app:login')
    template_name = 'accounts_app/register.html'


class AccountSettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts_app/account_settings.html"


class AccountChangeEmailView(LoginRequiredMixin, generic.FormView):
    template_name = "accounts_app/account_change_email.html"
    form_class = UserEmailChangeForm
    success_url = reverse_lazy("accounts_app:account_settings")

    def get_initial(self, *args, **kwargs):
        initial = super(AccountChangeEmailView, self).get_initial(**kwargs)
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        email_from_form = form.cleaned_data['email']

        user = self.request.user
        user_obj = User.objects.get(pk=user.pk)
        user_obj.email = email_from_form
        user_obj.save()

        return super(AccountChangeEmailView, self).form_valid(form)


class AccountChangePasswordView(LoginRequiredMixin, generic.FormView):
    template_name = "accounts_app/account_change_password.html"
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("accounts_app:account_settings")

    def form_valid(self, form):
        password_from_form = form.cleaned_data['password']

        user = self.request.user
        user_obj = User.objects.get(pk=user.pk)
        user_obj.set_password(raw_password=password_from_form)
        user_obj.save()

        return super(AccountChangePasswordView, self).form_valid(form)
