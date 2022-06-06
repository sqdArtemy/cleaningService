from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):  # Model for category of a service
    naming = models.CharField(verbose_name="Category name", max_length=100, null=False)

    def __str__(self):
        return self.naming


class Service(models.Model):  # Model for service of a company
    picture = models.ImageField(upload_to='services_pictures/', null=True, blank=True)
    name = models.CharField(verbose_name="Service name", max_length=256, null=False, unique=True)
    hours_required = models.FloatField(verbose_name="Hours required to complete this service",
                                       validators=(MinValueValidator(0),))
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=False)
    description = models.TextField(verbose_name="Description of a service", null=False)

    def __str__(self):
        return self.name




