import os

from django.core.exceptions import ImproperlyConfigured

from .settings import *  # noqa: F401,F403
from .settings import BASE_DIR


def get_env(name):
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"Environment variable {name} is required for production.")
    return value


def parse_azure_postgres_connection_string(connection_string):
    params = {}
    for part in connection_string.replace(";", " ").split():
        if "=" in part:
            key, value = part.split("=", 1)
            params[key.strip().lower()] = value.strip()
    return params


DEBUG = False

SECRET_KEY = get_env("SECRET")

# website_hostname = get_env("WEBSITE_HOSTNAME")
# allowed_hosts_value = os.environ.get("ALLOWED_HOSTS", website_hostname)
# ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_value.split(",") if host.strip()]
ALLOWED_HOSTS = [ os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

connection_string = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
parameters = parse_azure_postgres_connection_string(connection_string)

database_name = parameters.get("dbname") or parameters.get("database") or parameters.get("name")
database_host = parameters.get("host")
database_user = parameters.get("user")
database_password = parameters.get("password")
database_port = parameters.get("port", "5432")

missing = [
    key
    for key, value in {
        "dbname": database_name,
        "host": database_host,
        "user": database_user,
        "password": database_password,
    }.items()
    if not value
]
if missing:
    raise ImproperlyConfigured(
        "AZURE_POSTGRESQL_CONNECTIONSTRING is missing: " + ", ".join(missing)
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": database_name,
        "HOST": database_host,
        "USER": database_user,
        "PASSWORD": database_password,
        "PORT": database_port,
        "OPTIONS": {
            "sslmode": parameters.get("sslmode", "require"),
        },
    }
}
