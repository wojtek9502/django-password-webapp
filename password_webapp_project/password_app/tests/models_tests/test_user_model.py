from django.contrib.auth.models import User


def test_users_data_load(db, django_db_setup):
    users_list = User.objects.all()
    assert len(users_list) > 0
