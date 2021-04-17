from django.contrib import admin
from .models import Password

# Register your models here.


class PasswordAdmin(admin.ModelAdmin):
    pass
admin.site.register(Password, PasswordAdmin)


