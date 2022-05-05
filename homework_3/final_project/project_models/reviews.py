from datetime import datetime
from .profiles import *
from .request import *


class Review(models.Model):
    request = models.ForeignKey(to=Request, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    feedback = models.TimeField(verbose_name="Customer`s feedback")
    rate = models.PositiveIntegerField(verbose_name="Star-rating", default=0)
    created_at = models.DateTimeField(verbose_name="Time of creation", default=datetime.now())

    def __str__(self):
        return f"{self.request}-{self.rate}"