from django.db import models
from .countries import COUNTRIES
# Create your models here.


class Address(models.Model):
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=120, default='United Kingdom')
    post_code = models.CharField(max_length=200)

    def __str__(self):
        return self.city


class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    country = models.CharField(max_length=120, default='United Kingdom')
    sage_customer_id = models.CharField(max_length=50)
    address = models.ManyToManyField("Address", verbose_name="Addresses")

    def __str__(self):
        return "{} - {}".format(self.customer_name, self.country)
