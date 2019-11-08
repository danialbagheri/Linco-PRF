from django.urls import path, include
from django.conf.urls import url
from .views import home
urlpatterns = [
    path('', home)
]
