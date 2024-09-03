# Application definition

INSTALLED_APPS = [
    # user defined
    'chat.apps.main',

    # third party apps
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_filters',
    'daphne',
    'channels',

    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]
