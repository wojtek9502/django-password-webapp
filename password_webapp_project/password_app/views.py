from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from .forms import PasswordCreateForm
from .models import Password


class PasswordListView(generic.ListView):
    model = Password
    context_object_name = 'user_passwords'
    template_name = 'password_app/password_list.html'
    paginate_by = 10

    def get_queryset(self):
        curr_user_obj = self.request.user
        q_filter = Q(password_shared_users=curr_user_obj) | Q(password_owner=curr_user_obj)
        qs = Password.objects.filter(q_filter)
        return qs.order_by('description')


class PasswordDetailView(generic.DetailView):
    model = Password
    context_object_name = 'user_password'
    template_name = 'password_app/password_detail.html'


class PasswordCreateView(generic.CreateView):
    model = Password
    form_class = PasswordCreateForm
    template_name = 'password_app/password_create.html'

    def get_context_data(self, **kwargs):
        context = super(PasswordCreateView, self).get_context_data(**kwargs)
        curr_user_pk = self.request.user.pk
        context['form'].fields['password_shared_users'].queryset = User.objects.filter(~Q(pk=curr_user_pk))  # ~ means exclude
        return context


class PasswordUpdateView(generic.UpdateView):
    model = Password
    form_class = PasswordCreateForm
    template_name = "password_app/password_update.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordUpdateView, self).get_context_data(**kwargs)
        curr_user_pk = self.request.user.pk
        context['form'].fields['password_shared_users'].queryset = User.objects.filter(~Q(pk=curr_user_pk))  # ~ means exclude
        return context


class PasswordDeleteView(generic.DeleteView):
    model = Password
    template_name = "password_app/password_delete.html"
    context_object_name = "user_password"
    success_url = reverse_lazy('password_app:list')