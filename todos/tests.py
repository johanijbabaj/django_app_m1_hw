from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
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
