from django.db import models
import sys
sys.path.append("..")
from company.models import CompanyProfile


class Service(models.Model):  # model of service that companies provide
    name = models.CharField(verbose_name="Name of the service", max_length=256)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    service_image = models.ImageField(verbose_name="Image of a service", upload_to="images/service_images/")
    price = models.FloatField(verbose_name="Price of the service")
    deadline = models.IntegerField(verbose_name="Required hours to complete service")

    def __str__(self):
        return self.name
