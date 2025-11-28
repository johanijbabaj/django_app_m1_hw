from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import activate
from django.conf import settings
from datetime import date, timedelta
import json
from .models import Todo
from .forms import TodoForm, UserRegistrationForm


class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_todo_creation_with_all_fields(self):
        todo = Todo.objects.create(
            title='Test TODO',
            description='Test description',
            due_date=date.today() + timedelta(days=7),
            user=self.user
        )
        self.assertEqual(todo.title, 'Test TODO')
        self.assertEqual(todo.description, 'Test description')
        self.assertFalse(todo.is_completed)
        self.assertEqual(todo.user, self.user)

    def test_todo_creation_with_minimal_fields(self):
        todo = Todo.objects.create(
            title='Minimal TODO',
            user=self.user
        )
        self.assertEqual(todo.title, 'Minimal TODO')
        self.assertEqual(todo.description, '')
        self.assertIsNone(todo.due_date)
        self.assertFalse(todo.is_completed)

    def test_todo_string_representation(self):
        todo = Todo.objects.create(title='Test TODO', user=self.user)
        self.assertEqual(str(todo), 'Test TODO')

    def test_todo_user_association(self):
        todo = Todo.objects.create(title='User TODO', user=self.user)
        self.assertEqual(todo.user, self.user)
        self.assertIn(todo, self.user.todos.all())


class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.todo1 = Todo.objects.create(title='User1 TODO', user=self.user1)
        self.todo2 = Todo.objects.create(title='User2 TODO', user=self.user2)

    def test_list_view_shows_only_user_todos(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User1 TODO')
        self.assertNotContains(response, 'User2 TODO')

    def test_unauthenticated_user_redirected(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_create_todo_successfully(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('todo_create'), {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': date.today() + timedelta(days=5)
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='New TODO', user=self.user1).exists())

    def test_update_todo_successfully(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('todo_update', args=[self.todo1.pk]), {
            'title': 'Updated TODO',
            'description': 'Updated description'
        })
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Updated TODO')

    def test_delete_todo_successfully(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('todo_delete', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=self.todo1.pk).exists())

    def test_toggle_todo_completion(self):
        self.client.login(username='user1', password='pass123')
        self.assertFalse(self.todo1.is_completed)
        response = self.client.post(reverse('todo_toggle', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.is_completed)

    def test_cannot_access_other_user_todo(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('todo_update', args=[self.todo2.pk]))
        self.assertEqual(response.status_code, 403)


class TodoFormTest(TestCase):
    def test_valid_form_submission(self):
        form_data = {
            'title': 'Test TODO',
            'description': 'Test description',
            'due_date': date.today() + timedelta(days=7)
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_minimal_data(self):
        form_data = {'title': 'Minimal TODO'}
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_without_title(self):
        form_data = {'description': 'No title'}
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_due_date_not_required(self):
        form_data = {'title': 'No due date'}
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_user_logout(self):
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class InternationalizationTest(TestCase):
    """Test i18n features including language switching and translations"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_default_language_is_english(self):
        """Test that default language is English"""
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My TODOs')
        self.assertContains(response, 'Add TODO')

    def test_language_switcher_present(self):
        """Test that language switcher is present in navigation"""
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        # Check for language switcher - it uses i18n/setlang endpoint
        self.assertContains(response, '/i18n/')
        # Check for available languages
        self.assertContains(response, 'English')
        self.assertContains(response, 'Русский')
        self.assertContains(response, 'Español')
        self.assertContains(response, '中文')
        self.assertContains(response, 'Deutsch')

    def test_russian_translation(self):
        """Test that Russian translation works"""
        response = self.client.get('/ru/', HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(response.status_code, 200)
        # Check for Russian translated strings
        self.assertContains(response, 'Мои задачи')
        self.assertContains(response, 'Добавить задачу')

    def test_spanish_translation(self):
        """Test that Spanish translation works"""
        response = self.client.get('/es/', HTTP_ACCEPT_LANGUAGE='es')
        self.assertEqual(response.status_code, 200)
        # Check for Spanish translated strings
        self.assertContains(response, 'Mis Tareas')
        self.assertContains(response, 'Agregar Tarea')

    def test_chinese_translation(self):
        """Test that Chinese (Simplified) translation works"""
        response = self.client.get('/zh-hans/', HTTP_ACCEPT_LANGUAGE='zh-hans')
        self.assertEqual(response.status_code, 200)
        # Check for Chinese translated strings
        self.assertContains(response, '我的任务')
        self.assertContains(response, '添加任务')

    def test_german_translation(self):
        """Test that German translation works"""
        response = self.client.get('/de/', HTTP_ACCEPT_LANGUAGE='de')
        self.assertEqual(response.status_code, 200)
        # Check for German translated strings
        self.assertContains(response, 'Meine Aufgaben')
        self.assertContains(response, 'Aufgabe hinzufügen')

    def test_language_switching_via_post(self):
        """Test switching language via POST to set_language endpoint"""
        response = self.client.post('/i18n/setlang/', {
            'language': 'ru',
            'next': '/'
        })
        self.assertEqual(response.status_code, 302)
        # Follow redirect and check if language changed
        response = self.client.get('/ru/')
        self.assertContains(response, 'Мои задачи')

    def test_model_verbose_names_translatable(self):
        """Test that model verbose names are translatable"""
        activate('ru')
        todo = Todo.objects.create(title='Test', user=self.user)
        # Check that model meta verbose names are set
        self.assertEqual(Todo._meta.verbose_name, 'ЗАДАЧА')
        self.assertEqual(Todo._meta.verbose_name_plural, 'ЗАДАЧИ')
        activate('en')

    def test_form_labels_translatable(self):
        """Test that form field labels are translatable"""
        activate('ru')
        form = TodoForm()
        self.assertEqual(str(form.fields['title'].label), 'Название')
        self.assertEqual(str(form.fields['description'].label), 'Описание')
        activate('en')


class CalendarViewTest(TestCase):
    """Test calendar view and related functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        # Create test todos with different states
        self.active_todo = Todo.objects.create(
            title='Active TODO',
            description='Active task',
            due_date=date.today() + timedelta(days=5),
            user=self.user
        )

        self.completed_todo = Todo.objects.create(
            title='Completed TODO',
            description='Completed task',
            due_date=date.today() + timedelta(days=3),
            is_completed=True,
            user=self.user
        )

        self.overdue_todo = Todo.objects.create(
            title='Overdue TODO',
            description='Overdue task',
            due_date=date.today() - timedelta(days=2),
            user=self.user
        )

    def test_calendar_view_accessible(self):
        """Test that calendar view is accessible to logged-in users"""
        response = self.client.get(reverse('todo_calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar.html')

    def test_calendar_view_requires_login(self):
        """Test that calendar view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('todo_calendar'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_calendar_view_contains_fullcalendar(self):
        """Test that calendar view loads FullCalendar library"""
        response = self.client.get(reverse('todo_calendar'))
        self.assertEqual(response.status_code, 200)
        # Check for FullCalendar CDN links
        self.assertContains(response, 'fullcalendar')
        # Check for calendar container
        self.assertContains(response, 'id="calendar"')

    def test_calendar_api_endpoint_accessible(self):
        """Test that calendar API endpoint is accessible"""
        response = self.client.get(reverse('todo_calendar_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_calendar_api_returns_json(self):
        """Test that calendar API returns valid JSON"""
        response = self.client.get(reverse('todo_calendar_api'))
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)  # 3 todos created in setUp

    def test_calendar_api_event_structure(self):
        """Test that calendar API returns events with correct structure"""
        response = self.client.get(reverse('todo_calendar_api'))
        data = json.loads(response.content)

        # Check first event structure
        event = data[0]
        self.assertIn('id', event)
        self.assertIn('title', event)
        self.assertIn('start', event)
        self.assertIn('color', event)
        self.assertIn('extendedProps', event)

    def test_calendar_api_event_colors(self):
        """Test that calendar API assigns correct colors based on status"""
        response = self.client.get(reverse('todo_calendar_api'))
        data = json.loads(response.content)

        # Find events by title and check colors
        for event in data:
            if event['title'] == 'Completed TODO':
                # Completed todos should be green
                self.assertEqual(event['color'], '#10B981')
            elif event['title'] == 'Overdue TODO':
                # Overdue todos should be red
                self.assertEqual(event['color'], '#EF4444')
            elif event['title'] == 'Active TODO':
                # Active todos should be indigo
                self.assertEqual(event['color'], '#4F46E5')

    def test_calendar_api_only_user_todos(self):
        """Test that calendar API only returns current user's todos"""
        # Create another user and todo
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        Todo.objects.create(
            title='Other User TODO',
            user=other_user,
            due_date=date.today()
        )

        response = self.client.get(reverse('todo_calendar_api'))
        data = json.loads(response.content)

        # Should still only have 3 todos (from current user)
        self.assertEqual(len(data), 3)

        # Verify none of the todos belong to other user
        titles = [event['title'] for event in data]
        self.assertNotIn('Other User TODO', titles)

    def test_calendar_navigation_link_present(self):
        """Test that calendar navigation link is present in base template"""
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        # Check for calendar link in navigation
        self.assertContains(response, 'calendar')
        self.assertContains(response, 'Calendar')

    def test_calendar_toggle_on_home_page(self):
        """Test that home page has calendar toggle buttons"""
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        # Check for view toggle buttons
        self.assertContains(response, 'listViewBtn')
        self.assertContains(response, 'calendarViewBtn')
        # Check for inline calendar container
        self.assertContains(response, 'inlineCalendar')

    def test_calendar_legend_present(self):
        """Test that calendar page shows legend for event colors"""
        response = self.client.get(reverse('todo_calendar'))
        self.assertEqual(response.status_code, 200)
        # Check for legend
        self.assertContains(response, 'Legend')
        self.assertContains(response, 'Active')
        self.assertContains(response, 'Completed')
        self.assertContains(response, 'Overdue')
