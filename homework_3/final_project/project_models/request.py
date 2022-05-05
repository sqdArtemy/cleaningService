from django.db import models
from .profiles import User
from .service import Service

STATUSES = {  # Statuses of the request
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("canceled", "Canceled"),
}


class RequestStatus(models.Model):
    status = models.CharField(verbose_name="Request status", max_length=15, choices=STATUSES)

    def __str__(self):
        return self.status


class Request(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.ForeignKey(to=RequestStatus, on_delete=models.SET_NULL, null=True)
    total_area = models.FloatField(verbose_name="Total area to be cleaned", default=0)
    address = models.TimeField(verbose_name="User`s address")
    total_cost = models.FloatField(verbose_name="Final cost of the service")

    def __str__(self):
        return self.address