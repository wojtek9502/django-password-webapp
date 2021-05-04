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

## Config file

- go to directory with manage.py file inside
```sh
cd password_webapp_project/
````

- Create .env file...
```sh
vim .env
```

...containing the text below:

```text
SECRET_KEY=Test_Develop
DEBUG=True
STATIC_ROOT=static
MEDIA_ROOT=media

LANGUAGE_CODE=pl
TIME_ZONE=UTC
```
  

## Run
```shell
# in password_webapp_project dir
python manage.py runserver <ip:port>
```

## Test

Run tests
```shell
cd password_webapp_project
pytest
```