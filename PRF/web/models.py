from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
# from pif.models import Product, ProductVariant


class RequestType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Logs(models.Model):
    pass


'''
Production list are now delayed for a
'''
# class ProductionList(models.Model):

#     product = models.ForeignKey(
#         ProductVariant, on_delete=models.SET_NULL, null=True, related_name="product_variant")
#     quantity = models.PositiveIntegerField()
#     mfg_date = models.DateField(
#         auto_now=False, blank=True, null=True, help_text="For coding only")
#     expiry_date = models.DateField(
#         auto_now=False, blank=True, null=True, help_text="For coding only")
#     notes = models.TextField()

#     def __str__(self):
#         return self.product.product_code


class ProductionList(models.Model):
    '''
    Production list are now delayed for a
    '''
    product = models.CharField(max_length=200, blank=True, null=True,)
    quantity = models.PositiveIntegerField()
    mfg_date = models.DateField(
        auto_now=False, blank=True, null=True, help_text="For coding only")
    expiry_date = models.DateField(
        auto_now=False, blank=True, null=True, help_text="For coding only")
    notes = models.TextField()

    def __str__(self):
        return self.product


class ProductionJob(models.Model):
    SHRINK_WRAP = (
        ('Standard Clear', 'Standard Clear'),
        ('Black', 'Black'),
        ('Security Tape', 'Security Tape'),
    )
    STATUS = (
        ('Pending', 'Pending'),
        ('Open', 'Open'),
        ('Reviewing', 'Reviewing'),
        ('On-Hold', 'On-Hold'),
        ('Awaiting Information', 'Awaiting Information'),
        ('In progress', 'In progress'),
        ('Complete', 'Complete'),
    )
    PALLET_TYPE = (
        ('Standard', 'Standard'),
        ('Europe ', 'Europe'),
        ('Chap', 'Chap'),
        ('Heat Treated', 'Heat Treated'),
        ('Other', 'Other'),
    )
    prf_number = models.IntegerField(null=True, unique=True)
    customer_name = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_issued = models.DateField(auto_now_add=True)
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    customer_address_id = models.CharField(
        max_length=80, blank=True, null=True)
    request_type = models.ManyToManyField(RequestType, blank=True)
    date_issued = models.DateField(auto_now_add=True)
    required_date = models.DateField(auto_now_add=False)
    expected_completion_date = models.DateField(
        auto_now_add=True, blank=True, null=True)

    production_list = models.ManyToManyField(
        ProductionList, blank=True)
    pallet_type = models.CharField(
        max_length=30, choices=PALLET_TYPE, blank=True, null=True)
    expiry_date_format = models.CharField(
        max_length=30, blank=True, null=True)
    shrink_wrap = models.CharField(
        max_length=30, choices=SHRINK_WRAP, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=30, choices=STATUS, blank=True, null=True)
    address_label = models.BooleanField(default=False)
