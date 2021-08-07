from django.conf import settings


def pytest_configure():

    settings.configure(
        SECRET_KEY="fA794fWna94bqUlNStQGOli3uB2S1swUPFXwlvI3-Zf6rqsd6pJZ34iwbK34QaHM",
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.admin",
            "django.contrib.sessions",
            "django_inet",
        ],
        DATABASE_ENGINE="django.db.backends.sqlite3",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        LOGGING={
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "stderr": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                },
            },
            "loggers": {
                "": {"handlers": ["stderr"], "level": "DEBUG", "propagate": False},
            },
        },
    )
