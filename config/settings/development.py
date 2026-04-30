from .base import *  # noqa

DEBUG = True

# --- Arquivos estáticos em desenvolvimento ---
# Serve diretamente de STATICFILES_DIRS sem necessidade de collectstatic
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# --- Email ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Debug Toolbar (opcional, só ativa se instalado) ---
try:
    import debug_toolbar  # noqa
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
    INTERNAL_IPS = ["127.0.0.1", "172.0.0.0/8"]
except ImportError:
    pass

# --- Logs ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "format": "[{levelname}] {asctime} {module}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",  # Mude para DEBUG para logar todas as queries SQL
            "propagate": False,
        },
        "django.template": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}