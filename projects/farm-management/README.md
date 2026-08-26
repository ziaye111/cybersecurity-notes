# Farm Management

This project is a beginner-friendly Django farm-management application built in phases.

## Requirements

- Python 3.12+
- Django 6.1
- SQLite for local development

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install django
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Login and access

- Login page: /accounts/login/
- Dashboard: /

## Notes

- Keep the database local during development.
- Do not commit the virtual environment or the SQLite database.
