from django.contrib.auth.models import User
from django.db.models import Q
from django.views import generic

from .forms import PasswordCreateForm
from .models import Password


class PasswordListView(generic.ListView):
    model = Password
    context_object_name = 'user_passwords'
    template_name = 'password_app/password_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Password.objects.all()
        return qs


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
