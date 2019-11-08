from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=250)
    brand_color = models.CharField(max_length=10, help_text="HEX colour")

    def __str__(self):
        return self.name


class Component(models.Model):
    component_code = models.CharField(max_length=10)
    component_name = models.CharField(max_length=50)


PALLET_TYPE = (
    ('ST', 'STANDARD'),
    ('EU', 'EUROPE'),
)


class PalletInformation(models.Model):
    units_per_carton = models.PositiveIntegerField()
    cartons_per_layer = models.PositiveIntegerField()
    units_per_layer = models.PositiveIntegerField()
    layers_per_pallet = models.PositiveIntegerField()
    units_per_pallet = models.PositiveIntegerField()
    cartons_per_pallet = models.PositiveIntegerField()
    carton_weight = models.PositiveIntegerField(
        help_text="Only Integers. Unit=KG")
    carton_dimensions = models.PositiveIntegerField(
        help_text="Format= L x W x H , Unit=CM")
    pallet_weight_gross = models.PositiveIntegerField(help_text="Unit=KG")
    pallet_size = models.PositiveIntegerField(
        help_text="Format= L x W x H , Unit=CM")
    pallet_type = models.CharField(
        max_length=2, choices=PALLET_TYPE, default='ST')
    # pallet_wrapping = models.CharField(max_length=2)

    def __str__(self):
        return self.pallet_type


class ProductVariant(models.Model):
    product_code = models.CharField(max_length=10)
    option_name = models.CharField(max_length=20)
    option_value = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    barcode_number = models.PositiveIntegerField()
    box_of_6 = models.PositiveIntegerField()
    unit_dimensions = models.CharField(
        max_length=100, help_text="Format= L x W x H , Unit=CM")
    unit_weight = models.IntegerField(help_text="Unit=KG")
    date_first_available = models.DateField(auto_now=False, auto_now_add=False)
    discontinued = models.BooleanField(default=False)
    bills_of_component = models.ManyToManyField(Component, blank=True)
    pallet_information = models.ForeignKey(
        PalletInformation, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_code


class Product(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    slug = models.SlugField()
    variant = models.ManyToManyField(ProductVariant, blank=True)
    product_description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name
