from django.urls import path
from .views import profile_page, account_page

app_name = "profile_paths"
urlpatterns = [
    path("profile/", profile_page, name="profile_page"),
    path("account/", account_page, name="account_page"),
]
