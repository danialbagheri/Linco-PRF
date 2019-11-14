from django.urls import path, include
from django.conf.urls import url
from .views import home, product_request_form, add_customer


app_name = 'web'

urlpatterns = [
    path('', home),
    path('request-form/', product_request_form, name='request-form'),
    path('request-form/add-customer', add_customer, name='add-customer')
]
