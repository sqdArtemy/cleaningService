from django.db import models

class Address(models.Model):
    country = models.CharField(verbose_name="Country", max_length=100)
    city = models.CharField(verbose_name="City", max_length=100)
    address_line1 = models.CharField(verbose_name="Adress line 1 (District, Street)", max_length=150)
    address_line1 = models.CharField(verbose_name="Adress line 1 (District, Street)", max_length=150)