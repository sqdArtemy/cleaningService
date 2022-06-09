from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .profiles import User
from .request import Request


class Review(models.Model):
    request = models.ForeignKey(to=Request, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    feedback = models.TextField(verbose_name="Customer`s feedback", null=False)
    rate = models.PositiveSmallIntegerField(verbose_name="Star-rating", default=0, null=False, validators=(
        MaxValueValidator(5), MinValueValidator(0)))
    created_at = models.DateTimeField(verbose_name="Time of creation", default=timezone.now, null=False)

    def save(self, *args, **kwargs):
        # Set instance of customer instead of asking it from user
        self.customer = self.request.customer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request}-{self.rate}"
