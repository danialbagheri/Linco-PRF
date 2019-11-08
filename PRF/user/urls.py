from django.urls import include, path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'user'


urlpatterns = [
    url('login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    url('logout/', auth_views.LogoutView.as_view(
        template_name='accounts/logout.html'), name='logout'),
]
