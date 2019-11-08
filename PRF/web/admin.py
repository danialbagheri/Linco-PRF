from django.contrib import admin
from .models import ProductionList, RequestType, ProductionJob
# Register your models here.
admin.site.register(ProductionList)
admin.site.register(ProductionJob)
admin.site.register(RequestType)
