from django.db import models


class CompanyProfile(models.Model):  # model of a company
    name = models.CharField(verbose_name="Company name", max_length=100, unique=True)
    city = models.CharField(verbose_name="Company location city", max_length=100)
    rating = models.FloatField(verbose_name="Rating of the company", default=0)
    order_number = models.IntegerField(verbose_name="Number of completed orders", default=0)
    phone = models.CharField(verbose_name="Company`s phone number", max_length=100, unique=True)
    email = models.EmailField(verbose_name="Company`s email", unique=True)
    logo = models.ImageField(verbose_name="Logo of the company", upload_to="images/logos/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Company profiles"
