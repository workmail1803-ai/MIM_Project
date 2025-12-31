# Wond'r NEUB - Study Tour Booking System

This is a Django-based web application for managing study tour bookings for NEUB students.

## Prerequisites

*   Python 3.11 or higher
*   Git

## Local Setup Guide

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone <your-repo-url>
cd os_djangopro
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Database Setup

The project uses SQLite for local development (and PostgreSQL for production). Run the migrations to set up your local database:

```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin)

To access the admin panel, you need a superuser account:

```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

Start the local server:

```bash
python manage.py runserver
```

You should see output indicating the server is running at `http://127.0.0.1:8000/`.

### 7. Access the Application

*   **Home Page:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **Packages:** [http://127.0.0.1:8000/tourist-spots/packages/](http://127.0.0.1:8000/tourist-spots/packages/)
*   **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Troubleshooting

*   **SSL/HTTPS Errors:** If you get SSL errors locally, ensure `DEBUG` is set to `True` in `os_djangopro/settings.py` (this is the default for local env).
*   **Static Files:** If images don't load, ensure standard static files are collected or served correctly by Django (WhiteNoise is configured).

## Deployment

This project is configured for deployment on Railway. See `railway.json` and `Procfile` for configuration details.
