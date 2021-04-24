from django.views.generic import TemplateView


class AfterLogoutView(TemplateView):
    template_name = "accounts_app/after_logout.html"
