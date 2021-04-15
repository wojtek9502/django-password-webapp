from django.db import models
from django.contrib.auth.models import User


class Password(models.Model):
    description = models.CharField(max_length=500, default="")
    password = models.CharField(max_length=1000, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    password_owner = models.ForeignKey(User, default=None, null=True, related_name="owner", on_delete=models.CASCADE)
    password_shared_users = models.ManyToManyField(User, related_name="shared_users", blank=True)

    def __str__(self):
        return f"{self.description}, user: {self.password_owner.username}"

