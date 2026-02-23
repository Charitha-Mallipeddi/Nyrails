from django.urls import path

from .views import user_detail_view, user_redirect_view, user_update_view,user_autocomplete_view

app_name = "users"

urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~profile/", view=user_update_view, name="profile"),
    path("~autocomplete/", view=user_autocomplete_view, name="autocomplete"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
