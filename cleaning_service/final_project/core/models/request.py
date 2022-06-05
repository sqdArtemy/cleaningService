from django.db import models

from .profiles import User
from .service import Service

STATUSES = {  # Statuses of the request
    ("pending", "Pending"),
    ("accepted", "Accepted"),
    ("completed", "Completed"),
    ("canceled", "Canceled"),
}


class RequestStatus(models.Model):
    status = models.CharField(verbose_name="Request status", max_length=15, choices=STATUSES, null=False)

    def __str__(self):
        return self.status


class Request(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, related_name='Customer')
    status = models.ForeignKey(to=RequestStatus, on_delete=models.CASCADE, null=False)
    total_area = models.FloatField(verbose_name="Total area to be cleaned", default=0, null=False)
    country = models.CharField(verbose_name="Country of request", max_length=100, null=False)
    city = models.CharField(verbose_name="City of request", max_length=100, null=False)
    address_details = models.CharField(verbose_name="District, street, house, apartment", max_length=250, null=False)
    total_cost = models.FloatField(verbose_name="Final cost of the service", default=0)
    company = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='Company', null=True, blank=True)

    def __str__(self):
        return self.id
