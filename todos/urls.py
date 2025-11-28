from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('update/<int:pk>/', views.TodoUpdateView.as_view(), name='todo_update'),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='todo_delete'),
    path('toggle/<int:pk>/', views.toggle_todo, name='todo_toggle'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
