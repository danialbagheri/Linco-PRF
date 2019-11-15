from .views import all_customer_addresses
from django.urls import path, include
from django.conf.urls import url


app_name = 'customer'

urlpatterns = [
    path('address/<int:id>/', all_customer_addresses, name='address')
]
