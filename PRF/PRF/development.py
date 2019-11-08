import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['*']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w8m)o)$0yfrka6_l@h0#(rjwt)^2tmv3w!w+8+83w4)hcio314'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
