#Django password webapp

## Requirements
- Python 3.8

## Install
```sh
python -m pip install -r requirements.txt
cd password_webapp_project
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Run
```shell
# in password_webapp_project dir
python manage.py runserver
```

## Test

Run tests
```shell
cd password_webapp_project
pytest
```