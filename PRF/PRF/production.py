import os

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['accounts.pharmacistcoop.co.uk', '*.pharmacistcoop.co.uk']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'w8m)o)$0yfrka6_l@h0#(rjwt)^2tmv3w!w+8+83w4)hcio314')


EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'The PRF <admin@lincocare.com>'
CSRF_COOKIE_DOMAIN = '.lincocare.co.uk'
ADMINS = [('Danial', 'danial@lincocare.com'), ]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pharmacistcoop_django',
        'USER': 'dandelion',
        'PASSWORD': 'uygiyhopihghs',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
