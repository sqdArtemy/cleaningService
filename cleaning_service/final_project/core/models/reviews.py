from datetime import datetime
from .profiles import User
from .request import Request
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    request = models.ForeignKey(to=Request, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    feedback = models.TextField(verbose_name="Customer`s feedback", null=False)
    rate = models.PositiveSmallIntegerField(verbose_name="Star-rating", default=0, null=False, validators=(
        MaxValueValidator(5), MinValueValidator(0)))
    created_at = models.DateTimeField(verbose_name="Time of creation", default=datetime.now(), null=False)

    # Overloading save method in order to update company`s overall rating
    def save(self, *args, **kwargs):
        if self.request.company is not None:
            try:
                company_rating = self.request.company.rating
                if company_rating == 0:  # In case if this review is first for the company
                    self.request.company.rating = self.rate
                else:
                    self.request.company.rating = (self.rate + company_rating)/2
            except AttributeError:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request}-{self.rate}"
