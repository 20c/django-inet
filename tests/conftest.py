
from django.conf import settings


def pytest_configure():

    settings.configure(
        DEBUG=True,
        TEMPLATE_DEBUG=True,

        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django_blackhole',
        ],

        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },

        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'stderr': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    },
            },
            'loggers': {
                '': {
                    'handlers': ['stderr'],
                    'level': 'DEBUG',
                    'propagate': False
                },
            },
        },
    )

