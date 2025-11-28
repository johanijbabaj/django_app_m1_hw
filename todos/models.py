from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    due_date = models.DateField(_('due date'), null=True, blank=True)
    is_completed = models.BooleanField(_('is completed'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', verbose_name=_('user'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('TODO')
        verbose_name_plural = _('TODOs')

    def __str__(self):
        return self.title
