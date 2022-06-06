from django.db import models

from .profiles import User
from .request import Request


class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)  # User who retrieves notification
    seen = models.BooleanField(verbose_name="Notification was seen", default=False)
    header = models.CharField(verbose_name="Header of notification", max_length=156, null=False)
    text = models.TextField(verbose_name='Text of the notification', null=False)
    request = models.ForeignKey(to=Request, on_delete=models.CASCADE,  related_name='Request')
    accepted = models.BooleanField(verbose_name="Request was accepted", default=False)
