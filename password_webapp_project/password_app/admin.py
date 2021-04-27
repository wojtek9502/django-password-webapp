from django.contrib import admin
from .models import Password

# Register your models here.

@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    exclude = ('password',) # Don't show password field from Password model


