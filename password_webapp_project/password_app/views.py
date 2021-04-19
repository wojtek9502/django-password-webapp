from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

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
