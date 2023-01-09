"""{{cookiecutter.project_slug}} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

Inspired by https://github.com/cookiecutter/cookiecutter-django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/config/urls.py
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView

basic_urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
]

admin_urlpatterns = [
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path(settings.ADMIN_URL, admin.site.urls),
]

account_urlpatterns = [
    # User management
    path("users/", include("base.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
]

base_urlpatterns = [
    # base starter urls
    re_path(r"^base/", include("base.urls", namespace="base")),
]

custom_urlpatterns = [
    # Your stuff: custom urls includes go here
    # for django-tailwind browser reload
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns = basic_urlpatterns + \
    admin_urlpatterns + \
    account_urlpatterns + \
    base_urlpatterns + \
    custom_urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

