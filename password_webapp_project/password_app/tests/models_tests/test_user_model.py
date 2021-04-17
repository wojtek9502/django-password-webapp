from django.contrib.auth.models import User
from password_app.models import Password
from datetime import date

def test_users_data_load(db, django_db_setup):
    users_list = User.objects.all()
    assert len(users_list) > 0


def test_create_user(db, django_db_setup):
    user = User.objects.get(first_name="Admin")

    password = Password(
        description="Test password",
        password="Password",
        expiration_date = date.today(),
        password_owner=user
    )
    password.save()
    password_from_db = Password.objects.get(password_owner=user)

    assert password_from_db.description == "Test password"

def test_password_share(db, django_db_setup):
    user = User.objects.get(first_name="Admin")

    password = Password(
        description="Test password",
        password="Password",
        expiration_date=date.today(),
        password_owner=user
    )
    password.save()
    password.shared_users = [user]

    assert user in password.shared_users