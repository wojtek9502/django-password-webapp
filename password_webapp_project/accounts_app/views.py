from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import generic

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


class PasswordResetRequest(generic.View):

    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email_from_form = password_reset_form.cleaned_data['email']
            user_obj_qs = User.objects.filter(Q(email=email_from_form))

            if user_obj_qs.exists():
                for user_obj in user_obj_qs:
                    subject = "Resetowanie hasła"
                    email_template_name = "accounts_app/password_reset_email_body_template.txt"
                    mail_body = self.build_mail_body(request, user_obj, email_template_name)

                    try:
                        send_mail(subject, mail_body, 'reset_password@mail.com', [user_obj.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect(reverse_lazy("accounts_app:password_reset_done"))

    def get(self, request):
        password_reset_form = PasswordResetForm()

        return render(request=request, template_name="accounts_app/password_reset.html",
                      context={"form": password_reset_form})

    def build_mail_body(self, request, user_obj, email_template_name):
        c = {
            "email": user_obj.email,
            "full_name": user_obj.get_full_name(),
            'page_full_url': request.build_absolute_uri('/')[:-1],
            "uid": urlsafe_base64_encode(force_bytes(user_obj.id)),
            'token': default_token_generator.make_token(user_obj),
        }
        return render_to_string(email_template_name, c)
