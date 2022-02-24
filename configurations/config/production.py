from .base import *
from .db import POSTGRESQL

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = POSTGRESQL

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, '../static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

MEDIA_URL = '/media/'

