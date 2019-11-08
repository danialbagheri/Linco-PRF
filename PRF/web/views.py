from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

# Create your views here.


def home(request):
    return render(request, "home.html", context={})
