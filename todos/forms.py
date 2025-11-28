from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Todo


class TodoForm(forms.ModelForm):
    due_date = forms.DateField(
        label=_('Due Date'),
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date']
        labels = {
            'title': _('Title'),
            'description': _('Description'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': _('Enter todo title')
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': _('Enter todo description (optional)')
            }),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': _('Enter your email')
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _('Username'),
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': _('Choose a username')
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = _('Password')
        self.fields['password2'].label = _('Confirm Password')
        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': _('Enter password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': _('Confirm password')
        })
