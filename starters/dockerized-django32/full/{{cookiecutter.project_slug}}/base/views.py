from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from zen_queries import TemplateResponse as ZenTemplateResponse
from zen_queries import render as zen_render


def signup(request):
    """
    handles path("/signup/", signup, name="repos")
    """
    if request.method == "POST":
        # pylint: disable = no-value-for-parameter
        return login_create_session_post(request)
    return login_create_session_get(request)

@require_http_methods(["GET"])
def login_create_session_get(request):
    """
    handles GET request /login/
    """

    context = {}

    # TemplateResponse can only be rendered once
    return zen_render(request, "base/dashboard/login.html", context)

def signup(request):
    """
    handles path("/signup/", signup, name="repos")
    """
    if request.method == "POST":
        # pylint: disable = no-value-for-parameter
        return signup_create_account_post(request)
    return signup_create_account_get(request)

@require_http_methods(["GET"])
def signup_create_account_get(request):
    """
    handles GET request /signup/
    """

    context = {}

    # TemplateResponse can only be rendered once
    return zen_render(request, "base/dashboard/signup.html", context)