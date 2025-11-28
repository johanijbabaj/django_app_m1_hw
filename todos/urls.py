from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('update/<int:pk>/', views.TodoUpdateView.as_view(), name='todo_update'),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='todo_delete'),
    path('toggle/<int:pk>/', views.toggle_todo, name='todo_toggle'),
    path('calendar/', views.TodoCalendarView.as_view(), name='todo_calendar'),
    path('api/calendar/', views.todo_calendar_api, name='todo_calendar_api'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
