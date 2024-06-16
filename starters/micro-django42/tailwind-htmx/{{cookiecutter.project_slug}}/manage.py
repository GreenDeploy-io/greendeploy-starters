import os
import sys

from decouple import config
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse

BASE_DIR = os.path.dirname(__file__)

# Environment Variables
DEBUG = config("DEBUG", default=True, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="your_default_secret_key")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

# Django Settings
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
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
        # tailwind
        "tailwind",
        "theme",
        "django_browser_reload",
        # END tailwind
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
        # tailwind
        "django_browser_reload.middleware.BrowserReloadMiddleware",  # after any that encode the response, such as Django’s GZipMiddleware
        # END tailwind
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
    # Tailwind
    TAILWIND_APP_NAME="theme",
    INTERNAL_IPS=[
        "127.0.0.1",
    ],
    # END Tailwind
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


from django.shortcuts import render


def default(request):
    return render(request, "base.html")


# End of Views


# URL Patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", default),  # default
    # tailwind
    path("__reload__/", include("django_browser_reload.urls")),
    # END tailwind
    # because permanent=True, either purge the browser cache or use a different browser
    # if want to change
    # path("", lambda request: redirect("/hello/", permanent=True)),
    path("admin/", admin.site.urls),  # for admin
    path("hello/", hello_world),  # Updated path
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
