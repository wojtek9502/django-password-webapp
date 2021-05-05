from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import PasswordCreateForm
from .models import Password


class PasswordListView(LoginRequiredMixin, generic.ListView):
    model = Password
    context_object_name = 'user_passwords'
    template_name = 'password_app/password_list.html'
    paginate_by = 10

    def get_queryset(self):
        curr_user_obj = self.request.user
        q_filter = Q(password_shared_users=curr_user_obj) | Q(password_owner=curr_user_obj)
        qs = Password.objects.filter(q_filter).distinct()
        return qs.order_by('description')


class PasswordDetailView(LoginRequiredMixin, generic.DetailView):
    model = Password
    context_object_name = 'user_password'
    template_name = 'password_app/password_detail.html'


class PasswordCreateView(LoginRequiredMixin, generic.CreateView):
    model = Password
    form_class = PasswordCreateForm
    template_name = 'password_app/password_create.html'

    def get_context_data(self, **kwargs):
        context = super(PasswordCreateView, self).get_context_data(**kwargs)
        curr_user_pk = self.request.user.pk
        context['form'].fields['password_shared_users'].queryset = User.objects.filter(
            ~Q(pk=curr_user_pk))  # ~ means exclude
        return context

    def form_valid(self, form):
        shared_users_qs = form.cleaned_data['password_shared_users']
        self.object = form.save(commit=False)
        self.object.password_owner = self.request.user
        self.object.save()

        # Add shared users to password obj
        self.object.password_shared_users.add(*shared_users_qs)
        self.object.save()
        return HttpResponseRedirect(reverse_lazy("password_app:list"))


class PasswordUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Password
    form_class = PasswordCreateForm
    template_name = "password_app/password_update.html"
    success_url = reverse_lazy("password_app:list")

    def get(self, request, *args, **kwargs):
        request = super().get(request, *args, **kwargs)
        self.object = self.get_object()
        curr_user = self.request.user

        if curr_user is not self.request.user:
            if curr_user not in self.object.password_shared_users.all():
                return HttpResponseRedirect(reverse_lazy("password_app:list"))

        return request

    def get_context_data(self, **kwargs):
        context = super(PasswordUpdateView, self).get_context_data(**kwargs)
        curr_user = self.request.user

        # Don't show password owner user in shared users field
        context['form'].fields['password_shared_users'].queryset = User.objects.filter(
            ~Q(pk=curr_user.pk))  # ~ means exclude

        return context


class PasswordDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Password
    template_name = "password_app/password_delete.html"
    context_object_name = "user_password"
    success_url = reverse_lazy('password_app:list')


class RemoveUserFromSharedPasswordUsers(LoginRequiredMixin, generic.View):
    template_name = "password_app/password_remove_user_from_shared.html"

    def get(self, request, pk):
        current_user = self.request.user
        password_obj = Password.objects.get(pk=pk)

        if current_user not in password_obj.password_shared_users.all():
            return HttpResponseRedirect(reverse_lazy("password_app:list"))
        return render(request, self.template_name, {'password_obj': password_obj})

    def post(self, pk):
        current_user = self.request.user

        password_obj = Password.objects.get(pk=pk)
        if current_user in password_obj.password_shared_users.all():
            password_obj.password_shared_users.remove(current_user)
            password_obj.save()
        return HttpResponseRedirect(reverse_lazy("password_app:list"))
