"""
# BEGIN_REPLACE
# {{ cookiecutter.project_slug }} => {{ '{{ cookiecutter.project_slug }}' }}
# REPLACE_START
URL configuration for {{ cookiecutter.project_slug }} project.
# REPLACE_END

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/

Useful imports:
from django.urls import include, path

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

Influenced by https://github.com/cookiecutter/cookiecutter-django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/config/urls.py
"""
urlpatterns = []
