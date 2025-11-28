# Django TODO Application - ZoomCamp Module 1 Homework

A full-featured TODO application built with Django, featuring user authentication, CRUD operations, multi-language support, calendar view, and a modern Tailwind CSS interface.

## Features

### Core Features
- User registration and authentication
- Create, read, update, and delete TODOs
- Assign due dates to TODOs
- Mark TODOs as completed/incomplete
- Visual indicators for overdue items
- Responsive design with Tailwind CSS
- User-specific TODO lists (each user sees only their own TODOs)
- Admin panel for managing TODOs

### New Features
- **🌍 Multi-Language Support (i18n)**: Full internationalization with 5 languages
  - English (default)
  - Russian (Русский)
  - Spanish (Español)
  - Chinese Simplified (中文)
  - German (Deutsch)
  - Language switcher in navigation
  - Fully translated UI, forms, and messages

- **📅 Calendar View**: Interactive calendar for visualizing TODOs
  - Dedicated calendar page with FullCalendar.js integration
  - Inline calendar toggle on home page
  - Color-coded events:
    - 🟢 Green: Completed TODOs
    - 🔴 Red: Overdue TODOs
    - 🔵 Indigo: Active TODOs
  - Multiple view options (month, week, list)
  - Click events to edit TODOs
  - JSON API endpoint for calendar data

- **🎨 Custom Logo**: SVG-based scalable logo with favicon support

## Technology Stack

- Python 3.8+
- Django 4.2.26
- SQLite (database)
- Tailwind CSS (styling via CDN)
- FullCalendar.js 6.1.10 (calendar functionality)
- Django i18n framework (internationalization)
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

6. Compile translation messages (for multi-language support):
```bash
python manage.py compilemessages
```

7. Create a superuser (optional, for admin panel):
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

9. Access the application at: http://127.0.0.1:8000/
   - English version: http://127.0.0.1:8000/en/
   - Russian version: http://127.0.0.1:8000/ru/
   - Spanish version: http://127.0.0.1:8000/es/
   - Chinese version: http://127.0.0.1:8000/zh-hans/
   - German version: http://127.0.0.1:8000/de/

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

Our comprehensive test suite includes 38 tests covering:
- Model tests (creation, validation, string representation, i18n verbose names)
- View tests (CRUD operations, authentication, authorization)
- Form tests (validation, required fields, i18n labels)
- Authentication tests (registration, login, logout)
- **Internationalization tests** (language switching, translations, model/form labels)
- **Calendar tests** (views, API endpoint, event colors, user isolation, navigation)

## Project Structure

```
Homework/
├── manage.py
├── todo_project/          # Project configuration
│   ├── settings.py       # Main settings with i18n config (Q2 answer)
│   ├── urls.py           # URL patterns with i18n_patterns
│   ├── wsgi.py
│   └── asgi.py
├── todos/                 # Django app
│   ├── models.py         # TODO model with i18n verbose names
│   ├── views.py          # Business logic + calendar views (Q4 answer)
│   ├── forms.py          # Forms with i18n labels
│   ├── urls.py           # URL routing (incl. calendar routes)
│   ├── admin.py          # Admin panel configuration
│   ├── tests.py          # Test suite with i18n & calendar tests (Q6)
│   ├── static/           # Static files
│   │   └── todos/
│   │       └── images/
│   │           └── logo.svg  # Custom SVG logo
│   └── templates/        # HTML templates with i18n (Q5)
│       ├── base.html     # Base with logo & language switcher
│       ├── home.html     # List view + inline calendar toggle
│       ├── calendar.html # Dedicated calendar page
│       ├── todo_form.html
│       └── registration/
│           ├── login.html
│           └── register.html
├── locale/               # Translation files
│   ├── ru/LC_MESSAGES/   # Russian translations
│   ├── es/LC_MESSAGES/   # Spanish translations
│   ├── zh_Hans/LC_MESSAGES/  # Chinese translations
│   └── de/LC_MESSAGES/   # German translations
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

### Language Switching
- **Language Switcher**: Click the globe icon in the navigation bar
- **Select Language**: Choose from English, Russian, Spanish, Chinese, or German
- **Persistent Choice**: Language preference is remembered across sessions
- **Direct Access**: Use language-specific URLs (e.g., /ru/, /es/, /zh-hans/, /de/)

### Calendar View
- **Access Calendar**: Click "Calendar" in navigation or toggle on home page
- **View Modes**: Switch between month, week, and list views
- **Color Coding**:
  - Green events = Completed TODOs
  - Red events = Overdue TODOs
  - Blue events = Active TODOs
- **Edit TODOs**: Click any calendar event to edit that TODO
- **Inline Toggle**: On home page, switch between list and calendar view

### Admin Panel
Access at http://127.0.0.1:8000/admin/ (requires superuser account)

## Testing

Run the test suite (Question 6 answer):
```bash
python manage.py test
```

Expected output:
```
Found 38 test(s).
System check identified no issues (0 silenced).
Ran 38 tests in X.XXs
OK
```

Tests include:
- 14 original tests (models, views, forms, auth)
- 10 internationalization tests
- 14 calendar functionality tests

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
