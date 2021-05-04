from django import forms


class PasswordCsvFileUploadForm(forms.Form):
    csv_file = forms.FileField(label="", widget=forms.FileInput(attrs={'accept': ".csv"}))
