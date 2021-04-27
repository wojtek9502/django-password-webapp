from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Password(models.Model):
    description = models.CharField(verbose_name="Opis", max_length=500, default="")
    password = models.CharField(verbose_name="Hasło", max_length=1000, null=False, blank=False)
    expiration_date = models.DateField(verbose_name="Data wygaśnięcia", null=True, blank=True)
    create_date = models.DateField(verbose_name="Data utworzenia", auto_now_add=True)
    modify_date = models.DateField(verbose_name="Data modyfikacji", auto_now=True)
    password_owner = models.ForeignKey(User, verbose_name="Właściciel", default=None, null=True, related_name="+", on_delete=models.CASCADE)
    password_shared_users = models.ManyToManyField(User, verbose_name="Dziel hasło z", related_name="+", blank=True)

    class Meta:
        verbose_name = "Hasło"
        verbose_name_plural = "Hasła"


    def __str__(self):
        return f"{self.description}, user: {self.password_owner.username}"

    # Create and update views will be go to this page after form submit
    def get_absolute_url(self):
        return reverse('password_app:list', args=[str(self.pk)])

