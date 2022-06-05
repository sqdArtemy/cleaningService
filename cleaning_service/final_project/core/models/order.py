from django.db import models
from .notifications import Notification
from .profiles import User
from .request import Request


class Order(models.Model):
    notification = models.ForeignKey(to=Notification, on_delete=models.CASCADE, null=False)
    company = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='Company_order', null=True)
    request = models.ForeignKey(to=Request, on_delete=models.CASCADE, null=True, related_name='Request_order')
    total_cost = models.FloatField(verbose_name='Total cost of the order', default=0)
    accepted = models.BooleanField(verbose_name='Is order accepted by user', default=True)

    # Overloading method save for calculating total cost of the order and set some arguments
    def save(self, *args, **kwargs):
        # Set values to fields
        self.request = self.notification.request
        self.company = self.notification.request.company
        self.customer = self.notification.request.customer

        # Calculate cost of the service
        self.total_cost = float(self.notification.request.total_area) * \
                          float(self.notification.request.service.hours_required) * \
                          float(self.notification.user.hour_cost)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id
