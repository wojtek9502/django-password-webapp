from django.urls import path

from . import views

app_name = 'password_import_export_app'
urlpatterns = [
    path('export_csv/', views.PasswordExportToCSV.as_view(), name='export_to_csv'),
    path('import_csv/upload/', views.PasswordImportFromCsvFile.as_view(), name='import_from_csv_upload'),
    path('import_csv/load/', views.PasswordImportFromCsvFileLoadData.as_view(), name='import_from_csv_load'),
]
