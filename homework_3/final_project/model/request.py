from django.db import models
from .profiles import User
from .service import Service

STATUSES = {  # Statuses of the request
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("canceled", "Canceled"),
}


class RequestStatus(models.Model):
    status = models.CharField(verbose_name="Request status", max_length=15, choices=STATUSES, null=False)

    def __str__(self):
        return self.status


class Request(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(to=RequestStatus, on_delete=models.CASCADE, null=False)
    total_area = models.FloatField(verbose_name="Total area to be cleaned", default=0, null=False)
    address = models.TimeField(verbose_name="User`s address", null=False)
    total_cost = models.FloatField(verbose_name="Final cost of the service", null=False)

    def __str__(self):
        return self.address