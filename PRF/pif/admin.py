from django.contrib import admin
from .models import (
    Brand,
    Component,
    PalletInformation,
    ProductVariant,
    Product,
)
# Register your models here.


admin.site.register(Brand)
admin.site.register(Component)
admin.site.register(PalletInformation)
admin.site.register(ProductVariant)
admin.site.register(Product)
