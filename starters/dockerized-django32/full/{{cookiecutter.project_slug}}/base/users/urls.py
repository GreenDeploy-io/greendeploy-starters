from base.users.views import user_detail_view, user_redirect_view, user_update_view
from django.urls import path

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:id>/", view=user_detail_view, name="detail"),
]
