import csv
import json
from typing import List, Dict, Tuple

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from password_app.models import Password
from .forms import PasswordCsvFileUploadForm
from .utils.password_export_import_utils import parse_password_to_csv_file, csv_fieldnames_list, \
    csv_required_fields_list


class PasswordExportToCSV(generic.View):
    def get(self, request):
        # Get user passwords
        curr_user_obj = self.request.user
        q_filter = Q(password_shared_users=curr_user_obj) | Q(password_owner=curr_user_obj)
        passwords_qs = Password.objects.filter(q_filter).distinct()

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="passwords_{curr_user_obj}.csv"'

        # write to csv file
        writer = csv.DictWriter(response, fieldnames=csv_fieldnames_list, delimiter=";")
        writer.writeheader()

        for password in passwords_qs:
            row_dict = parse_password_to_csv_file(password, csv_fieldnames_list)
            writer.writerow(row_dict)

        return response


class PasswordImportFromCsvFile(generic.FormView):
    form_class = PasswordCsvFileUploadForm
    template_name = "password_import_export_app/password_csv_import_upload.html"

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
                    template_name="password_import_export_app/password_csv_import_validate_error.html",
                    context={"validate_errors_list": validate_errors_list,
                             "upload_file_rows": upload_file_rows}
                )

            return render(
                request,
                template_name="password_import_export_app/password_csv_import_validate_ok.html",
                context={"upload_file_rows": upload_file_rows,
                         "upload_file_rows_json": upload_file_rows_json}
            )

    def parse_file_rows(self, file, delimiter=";", encoding="utf-8") -> Tuple[List, List[Dict]]:
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
        return fieldnames, rows_list

    def validate_csv_rows(self, fieldnames_from_file, upload_file_rows: dict):
        errors_list = []

        if fieldnames_from_file != csv_fieldnames_list:
            errors_list.append("Niewłaściwy nagłówek pliku CSV")

        for row_n, file_row in enumerate(upload_file_rows, start=1):
            if len(file_row.keys()) != len(fieldnames_from_file):
                errors_list.append(f"Błąd w wierszu nr {row_n}: Niewłaściwa liczba kolumn w wierszu")

            for required_csv_field in csv_required_fields_list:
                if not len(file_row.get(required_csv_field)):
                    errors_list.append(
                        f"Błąd w wierszu nr {row_n}: Brak wartości dla kolumny \"{required_csv_field}\", w wierszu.")

        return errors_list


class PasswordImportFromCsvFileLoadData(generic.TemplateView):

    def post(self, request):
        csv_file_import_data_json = json.loads(request.POST['csv_import_data_json'])

        for password_data_from_csv in csv_file_import_data_json:
            password_owner_username_from_csv = password_data_from_csv.get("password_owner")
            try:
                password_owner_obj = User.objects.get(username=password_owner_username_from_csv)
            except ObjectDoesNotExist:
                continue

            password_obj, is_obj_created = Password.objects.get_or_create(
                description=password_data_from_csv.get("description"),
                password=password_data_from_csv.get("password"),
                expiration_date=password_data_from_csv.get("expiration_date"),
                password_owner=password_owner_obj
            )

            # Add shared users from CSV to password object
            password_shared_users = self.get_password_shared_users_from_csv(password_data_from_csv)
            if is_obj_created and password_shared_users:
                password_obj.password_shared_users.add(*password_shared_users)

        return render(request, "password_import_export_app/password_csv_import_load_success.html",
                      context={
                          "csv_file_import_data_json": csv_file_import_data_json
                      })

    def get_password_shared_users_from_csv(self, password_data_from_csv):
        password_shared_users_from_csv = password_data_from_csv.get("password_shared_users")
        password_shared_users_list = []

        # Parse shared_users from csv to model objects
        if password_shared_users_from_csv != "-":
            password_shared_users_from_csv = password_shared_users_from_csv.split(",")
            for user in password_shared_users_from_csv:
                try:
                    shared_user = User.objects.get(username=user)
                except ObjectDoesNotExist:
                    continue
                password_shared_users_list.append(shared_user)

        return password_shared_users_list if len(password_shared_users_list) > 0 else False
