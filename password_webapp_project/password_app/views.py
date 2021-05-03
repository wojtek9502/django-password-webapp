import csv, json
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import PasswordCreateForm, PasswordCsvFileUploadForm
from .models import Password
from .utils.password_export_utils import parse_password_to_csv_file


class PasswordListView(generic.ListView):
    model = Password
    context_object_name = 'user_passwords'
    template_name = 'password_app/password_list.html'
    paginate_by = 10

    def get_queryset(self):
        curr_user_obj = self.request.user
        q_filter = Q(password_shared_users=curr_user_obj) | Q(password_owner=curr_user_obj)
        qs = Password.objects.filter(q_filter).distinct()
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


class PasswordUpdateView(generic.UpdateView):
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


class PasswordDeleteView(generic.DeleteView):
    model = Password
    template_name = "password_app/password_delete.html"
    context_object_name = "user_password"
    success_url = reverse_lazy('password_app:list')


class RemoveUserFromSharedPasswordUsers(generic.View):
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


class PasswordExportToCSV(generic.View):
    def get(self, request):
        # Get user passwords
        curr_user_obj = self.request.user
        q_filter = Q(password_shared_users=curr_user_obj) | Q(password_owner=curr_user_obj)
        passwords_qs = Password.objects.filter(q_filter).distinct()
        fieldnames = ["description", "password", "expiration_date", "password_owner", "password_shared_users"]

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="passwords_{curr_user_obj}.csv"'

        # write to csv file
        writer = csv.DictWriter(response, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for password in passwords_qs:
            row_dict = parse_password_to_csv_file(password, fieldnames)
            writer.writerow(row_dict)

        return response


class PasswordImportFromCsvFile(generic.FormView):
    form_class = PasswordCsvFileUploadForm
    template_name = "password_app/password_csv_import_upload.html"

    def post(self, request, *args, **kwargs):
        # if not len(request.FILES):
        #     return HttpResponseRedirect(reverse_lazy("password_app:list"))

        form = PasswordCsvFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fieldnames, upload_file_rows = self.parse_file_rows(request.FILES['csv_file'])
            validate_errors_list = self.validate_csv_rows(fieldnames, upload_file_rows)

            upload_file_rows_json = json.dumps(upload_file_rows)
            if len(validate_errors_list):
                return render(
                    request,
                    template_name="password_app/password_csv_import_validate_error.html",
                    context={"validate_errors_list": validate_errors_list,
                             "upload_file_rows": upload_file_rows}
                )

            return render(
                request,
                template_name="password_app/password_csv_import_validate_ok.html",
                context={"upload_file_rows": upload_file_rows,
                         "upload_file_rows_json": upload_file_rows_json}
            )

    def parse_file_rows(self, file, delimiter=";", encoding="utf-8"):
        rows_list = []
        fieldnames = []
        for i, row in enumerate(file):
            row = row.decode(encoding).replace("\r\n", "")  # rsplit remove endline chars
            row = row.split(delimiter)
            row = [col.strip() for col in row]
            if i == 0:
                fieldnames = row
            else:
                csv_row = dict(zip(fieldnames, row))
                rows_list.append(csv_row)
        return fieldnames,  rows_list

    def validate_csv_rows(self, fieldnames, upload_file_rows: dict):
        errors_list = []
        required_fieldnames = ["description", "password", "expiration_date", "password_owner", "password_shared_users"]

        if required_fieldnames != fieldnames:
            errors_list.append("Niewłaściwy nagłówek pliku CSV")

        for row_n, file_row in enumerate(upload_file_rows, start=1):
            if len(file_row.keys()) != len(required_fieldnames):
                errors_list.append(f"Błąd w wiersz pliku: {row_n}: Niewłaściwa liczba kolumn w wierszu")
        return errors_list


class PasswordImportFromCsvFileLoadData(generic.TemplateView):

    def post(self, requset):
        csv_file_import_data_json = json.loads(requset.POST['csv_import_data_json'])

        for password_data in csv_file_import_data_json:
            obj, is_obj_created = Password.objects.get_or_create(
                description=password_data.get("description"),
                password=password_data.get("password"),
                expiration_date=password_data.get("expiration_date"),
                password_owner=User.objects.get(username=password_data.get("password_owner"))
            )

            if is_obj_created:
                if password_data.get("password_shared_users") != "-":
                    password_shared_users_list = password_data.get("password_shared_users").split(",")
                    for user in password_shared_users_list:
                        shared_user = User.objects.get(username=user)
                        if shared_user:
                            obj.password_shared_users.add(shared_user)
                    obj.save()

        return render(requset, "password_app/password_csv_import_load_success.html",
                      context={
                          "csv_file_import_data_json": csv_file_import_data_json
                      })
