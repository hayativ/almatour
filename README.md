# Almatour API

Almatour is a tourism guide for Almaty, providing information about places, events, and souvenirs.

## Setup

1. Create a virtual environment:
   ```bash
   python3.14 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API documentation is available at `/api/schema/swagger-ui/`.