"""Swerl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from .views import MySignupView, MyLoginView, ChangePasswordDone
from django.contrib.auth.views import LogoutView

admin.site.site_header = 'Swerl'                    # default: "Django Administration"
admin.site.index_title = 'Swerl Admin Area'                 # default: "Site administration"
admin.site.site_title = 'Swerl Admin' # default: "Django site admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("expenses.urls")),
    path("signup", MySignupView.as_view(), name="signup_page"),
    path("login", MyLoginView.as_view(), name="login_page"),
    path("signup/", RedirectView.as_view(url="/signup")),
    path("login/", RedirectView.as_view(url="/login")),
    path("logout", LogoutView.as_view()),
    path("", include("swerl_profile.urls")),
    path("password-change", auth_views.PasswordChangeView.as_view(success_url="password-change/done/"), name="password_change"),
    path("password-change/", RedirectView.as_view(url="/password-change")),
    path("password-change/done/", ChangePasswordDone),
]
