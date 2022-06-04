from django.db import models

class Category(models.Model):  # Model for category of a service
    naming = models.CharField(verbose_name="Category name", max_length=100, null=False)

    def __str__(self):
        return self.naming


class Service(models.Model):  # Model for service of a company
    picture = models.ImageField(upload_to='services_pictures/', null=True, blank=True)
    name = models.CharField(verbose_name="Service name", max_length=256, null=False)
    cost = models.FloatField(verbose_name="Cost of service per m^2", default=0, null=False)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name




