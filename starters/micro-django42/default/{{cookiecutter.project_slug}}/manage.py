import os
import sys

# this ensures that the .env file is loaded from the correct location
from decouple import Config, RepositoryEnv
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse  # Updated to use JsonResponse
from django.shortcuts import redirect
from django.urls import path


def get_config():

    # Default to 'local' if ENV_NAME not set
    env_name = os.getenv("ENV_NAME", "local")

    # in the production environment, make sure to set ENV_NAME to 'production'
    env_file = f".env.{env_name}"
    return Config(RepositoryEnv(env_file))


config = get_config()

BASE_DIR = os.path.dirname(__file__)

# Environment Variables
DEBUG = config("DEBUG", default=True, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="your_default_secret_key")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

# Default to 'local' if ENV_NAME not set
env_name = os.getenv("ENV_NAME", "local")
if env_name == "local":

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Django Settings
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    STATIC_URL="/static/",
    STATIC_ROOT=os.path.join(BASE_DIR, "staticfiles"),
    STATICFILES_DIRS=[os.path.join(BASE_DIR, "static")],
    INSTALLED_APPS=[
        # compulsory
        "django.contrib.auth",  # For user authentication
        "django.contrib.contenttypes",  # For content types used by the authentication system
        "django.contrib.sessions",  # For session management, required if using session-based authentication
        "django.contrib.staticfiles",  # For serving static files
        # END compulsory
        "django.contrib.admin",  # for admin
        "django.contrib.messages",  # for admin
    ],
    ROOT_URLCONF=__name__,
    LOGIN_URL="/admin/login/",  # for auth but using admin
    MIDDLEWARE=[
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",  # Required for admin
        "django.contrib.auth.middleware.AuthenticationMiddleware",  # Required for admin
        "django.contrib.messages.middleware.MessageMiddleware",  # Required for admin
    ],
    # Templates
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
            "APP_DIRS": True,  # Add this line to enable template loading from plugins
            "OPTIONS": {
                "context_processors": [
                    # ... other context processors ...
                    "django.template.context_processors.debug",  # for admin
                    "django.template.context_processors.request",  # for admin
                    "django.contrib.auth.context_processors.auth",  # for admin
                    "django.contrib.messages.context_processors.messages",  # for admin
                ],
            },
        },
    ],
)


# Ensure django fully utilized before models, etc
import django

django.setup()
# End


# Serializers
# ----


# end of serializers


# Views
def hello_world(request):
    return JsonResponse({"message": "Hello, World!"})  # Updated endpoint function


# End of Views


# URL Patterns

from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path("", lambda request: redirect("/hello/", permanent=True)),
    path("admin/", admin.site.urls),  # for admin
    path("hello/", hello_world),  # Updated path
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
