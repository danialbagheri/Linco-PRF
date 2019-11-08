from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from customer.models import Customer
from pif.models import Product, ProductVariant


class RequestType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductionList(models.Model):
    product = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, related_name="product_variant")
    quantity = models.PositiveIntegerField()
    mfg_date = models.DateField(
        auto_now=False, blank=True, null=True, help_text="For coding only")
    expiry_date = models.DateField(
        auto_now=False, blank=True, null=True, help_text="For coding only")
    notes = models.TextField()

    def __str__(self):
        return self.product.product_code


SHRINK_WRAP = (
    ('ST', 'STANDARD CLEAR'),
    ('BL', 'Black'),
    ('ST', 'Security Tape'),
)

STATUS = (
    ('PE', 'Pending'),
    ('OP', 'Open'),
    ('RE', 'Reviewing'),
    ('OH', 'On-Hold'),
    ('AI', 'Awaiting Information'),
    ('PR', 'In progress'),
    ('CO', 'Complete'),
)


class ProductionJob(models.Model):
    prf_number = models.IntegerField()
    customer_name = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_issued = models.DateField(auto_now_add=True)
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    request_type = models.ManyToManyField(RequestType, blank=True)
    date_issued = models.DateField(auto_now_add=True)
    required_date = models.DateField(auto_now_add=True)
    expected_completion_date = models.DateField(
        auto_now_add=True, blank=True, null=True)
    production_list = models.ManyToManyField(
        ProductionList, blank=True)
    # pallet_type = models.CharField(
    #     max_length=2, choices=PALLET_TYPE, blank=True, null=True)
    expiry_date_format = models.CharField(
        max_length=10, blank=True, null=True)
    shrink_wrap = models.CharField(
        max_length=2, choices=SHRINK_WRAP, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=STATUS, blank=True, null=True)
