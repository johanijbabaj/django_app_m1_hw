from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Todo
from .forms import TodoForm, UserRegistrationForm


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'home.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo_form.html'
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo_form.html'
    success_url = reverse_lazy('todo_list')

    def test_func(self):
        todo = self.get_object()
        return todo.user == self.request.user


class TodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy('todo_list')

    def test_func(self):
        todo = self.get_object()
        return todo.user == self.request.user


@login_required
def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('todo_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('todo_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class TodoCalendarView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'calendar.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


@login_required
def todo_calendar_api(request):
    """API endpoint for FullCalendar to fetch events"""
    todos = Todo.objects.filter(user=request.user)
    events = []

    for todo in todos:
        # Determine event color based on status
        if todo.is_completed:
            color = '#10B981'  # Green for completed
        elif todo.due_date and todo.due_date < timezone.now().date():
            color = '#EF4444'  # Red for overdue
        else:
            color = '#4F46E5'  # Indigo for active

        event = {
            'id': todo.pk,
            'title': todo.title,
            'start': todo.due_date.isoformat() if todo.due_date else timezone.now().date().isoformat(),
            'color': color,
            'extendedProps': {
                'description': todo.description,
                'is_completed': todo.is_completed,
            }
        }
        events.append(event)

    return JsonResponse(events, safe=False)
