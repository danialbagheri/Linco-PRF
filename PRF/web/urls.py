from django.urls import path, include
from django.conf.urls import url
from .views import home, product_request_form, add_customer, all_jobs, user_jobs


app_name = 'web'

urlpatterns = [
    path('', home),
    path('request-form/', product_request_form, name='request-form'),
    path('request-form/add-customer', add_customer, name='add-customer'),
    path('jobs/all-jobs/', all_jobs, name="all-jobs"),
    path('jobs/user_jobs/', user_jobs, name="user-jobs")
]
