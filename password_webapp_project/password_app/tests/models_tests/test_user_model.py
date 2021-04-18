import pytest
from datetime import date

from django.contrib.auth.models import User
from password_app.models import Password


def test_users_data_load(db, django_db_setup):
    users_list = User.objects.all()
    assert len(users_list) > 0


def test_create_user(db, django_db_setup):
    user = User.objects.get(first_name="Admin")
    expected = "Test password"

    password = Password(
        description="Test password",
        password="Password",
        expiration_date = date.today(),
        password_owner=user
    )
    password.save()
    password_from_db = Password.objects.get(password_owner=user)

    assert password_from_db.description == expected

def test_password_share(db, django_db_setup):
    user = User.objects.get(first_name="Admin")
    expected_users = [user]

    password = Password(
        description="Test password",
        password="Password",
        expiration_date=date.today(),
        password_owner=user
    )
    password.save()
    password.shared_users = [user]

    assert password.shared_users == expected_users

def test_password_share_with_many_users(db, django_db_setup):
    user1 = User.objects.get(first_name="Admin")
    user2 = User.objects.get(first_name="test")
    expected_users = [user1, user2]

    password = Password(
        description="Test password",
        password="Password",
        expiration_date=date.today(),
        password_owner=user1
    )
    password.save()
    password.shared_users = [user1, user2]

    assert password.shared_users == expected_users

def test_two_owners_of_password(db, django_db_setup):
    user1 = User.objects.get(first_name="Admin")
    user2 = User.objects.get(first_name="test")

    with pytest.raises(ValueError):
        password = Password(
            description="Test password",
            password="Password",
            expiration_date=date.today(),
            password_owner=[user1, user2]
        )

