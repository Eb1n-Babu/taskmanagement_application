# Task Management Application

A Django-based app for task assignment, completion with reports/hours, and admin panel.

## Setup
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py createsuperuser
4. python manage.py runserver

## Testing
- API: Use Postman collection (exported as taskmanagement.postman_collection.json)
- Django: python manage.py test

## Features
- JWT API for users
- Custom admin panel for roles/tasks