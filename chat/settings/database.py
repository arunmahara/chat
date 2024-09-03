from .base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },

    # Uncomment the following to use PostgreSQL
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.getenv('POSTGRES_DB'),
    #     'USER': os.getenv('POSTGRES_USER'),
    #     'HOST': os.getenv('POSTGRES_HOST'),
    #     'PORT': os.getenv('POSTGRES_PORT'),
    #     'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    # },

}
