# Erp - Django
## Create a virtual environment with python 3.7
``python3 -m venv venv ``

## Activate a virtual environment
``source venv/bin/activate ``

## Install requirements
``pip install -r requirements/local.txt ``

## Create migrations
``python manage.py makemigrations ``

## Apply
``python manage.py migrate ``

## Create superuser
``python manage.py createsuperuser ``

## Run server
``python manage.py runserver ``

