from datetime import datetime
from .profiles import User
from .request import Request
from django.db import models


class Review(models.Model):
    request = models.ForeignKey(to=Request, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    feedback = models.TextField(verbose_name="Customer`s feedback", null=False)
    rate = models.PositiveIntegerField(verbose_name="Star-rating", default=0, null=False)
    created_at = models.DateTimeField(verbose_name="Time of creation", default=datetime.now(), null=False)

    def __str__(self):
        return f"{self.request}-{self.rate}"
