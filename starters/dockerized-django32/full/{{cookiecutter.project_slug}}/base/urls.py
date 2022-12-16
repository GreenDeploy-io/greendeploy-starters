from base.views import login, signup
from django.urls import path

app_name = "base"
urlpatterns = [
    path("~signup/", view=login, name="login"),
    path("~login/", view=signup, name="signup"),
]
