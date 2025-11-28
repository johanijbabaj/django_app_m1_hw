# Django TODO Application - ZoomCamp Module 1 Homework

A full-featured TODO application built with Django, featuring user authentication, CRUD operations, and a modern Tailwind CSS interface.

## Features

- User registration and authentication
- Create, read, update, and delete TODOs
- Assign due dates to TODOs
- Mark TODOs as completed/incomplete
- Visual indicators for overdue items
- Responsive design with Tailwind CSS
- User-specific TODO lists (each user sees only their own TODOs)
- Admin panel for managing TODOs

## Technology Stack

- Python 3.8+
- Django 4.2.26
- SQLite (database)
- Tailwind CSS (styling)
- uv (package manager)

## Installation

### Prerequisites

- Python 3.8 or higher
- uv package manager

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/johanijbabaj/django_app_m1_hw.git
cd django_app_m1_hw
```

2. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or on macOS with Homebrew:
# brew install uv
```

3. Create virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install Django (Question 1 answer):
```bash
uv pip install django
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional, for admin panel):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the application at: http://127.0.0.1:8000/

## Homework Questions & Answers

### Question 1: Install Django

**Command used:**
```bash
uv pip install django
```

This command uses the uv package manager (as recommended in the homework) to install Django in the virtual environment.

### Question 2: Project and App

**Answer: `settings.py`**

After creating the Django project and app, you need to edit the `settings.py` file to include the app in the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todos',  # Our TODO app
]
```

### Question 3: Django Models

**Answer: Run migrations**

After defining the models in `models.py`, the next step is to create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the database tables based on the model definitions.

### Question 4: TODO Logic

**Answer: `views.py`**

The business logic for the TODO app is implemented in `views.py`. This file contains:
- TodoListView - Display user's TODOs
- TodoCreateView - Create new TODO
- TodoUpdateView - Edit existing TODO
- TodoDeleteView - Delete TODO
- toggle_todo function - Toggle completion status
- Authentication views (register, login)

### Question 5: Templates

**Answer: `TEMPLATES['DIRS']` in project's `settings.py`**

To register the directory with templates, you need to modify the `TEMPLATES` setting in `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'todos' / 'templates'],  # Template directory
        'APP_DIRS': True,
        # ... rest of configuration
    },
]
```

### Question 6: Tests

**Answer: `python manage.py test`**

This is Django's built-in test runner command. It runs all tests in the project:

```bash
python manage.py test
```

Our test suite includes 18 tests covering:
- Model tests (creation, validation, string representation)
- View tests (CRUD operations, authentication, authorization)
- Form tests (validation, required fields)
- Authentication tests (registration, login, logout)

## Project Structure

```
Homework/
├── manage.py
├── todo_project/          # Project configuration
│   ├── settings.py       # Main settings (Q2 answer)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── todos/                 # Django app
│   ├── models.py         # TODO model
│   ├── views.py          # Business logic (Q4 answer)
│   ├── forms.py          # TodoForm and UserRegistrationForm
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin panel configuration
│   ├── tests.py          # Test suite (Q6)
│   └── templates/        # HTML templates (Q5)
│       ├── base.html
│       ├── home.html
│       ├── todo_form.html
│       └── registration/
│           ├── login.html
│           └── register.html
├── .gitignore
└── README.md
```

## Usage

### User Registration
1. Navigate to http://127.0.0.1:8000/register/
2. Create a new account with username, email, and password

### Login
1. Navigate to http://127.0.0.1:8000/login/
2. Enter your credentials

### Managing TODOs
- **View TODOs**: Home page displays all your TODOs
- **Create TODO**: Click "+ Add TODO" button
- **Edit TODO**: Click "Edit" button on any TODO
- **Delete TODO**: Click "Delete" button (with confirmation)
- **Toggle Completion**: Click the circle icon next to TODO title
- **Due Dates**: Overdue TODOs are highlighted in red

### Admin Panel
Access at http://127.0.0.1:8000/admin/ (requires superuser account)

## Testing

Run the test suite (Question 6 answer):
```bash
python manage.py test
```

Expected output:
```
Found 18 test(s).
Ran 18 tests in X.XXs
OK
```

## Security Features

- CSRF protection enabled
- Password hashing with Django's built-in system
- User authentication required for all TODO operations
- SQL injection prevention through Django ORM
- XSS protection through template auto-escaping
- User isolation (users can only access their own TODOs)

## License

This project was created for educational purposes as part of ZoomCamp Module 1 Homework.

## Author

Created with AI assistance using Claude Code
