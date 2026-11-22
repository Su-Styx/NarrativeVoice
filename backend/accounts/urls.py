from django.urls import path
from . import views

urlpatterns = [
    path("csrf/", views.csrf),
    path("me/", views.me),
    path("register/", views.register),
    path("login/", views.login_check),
    path("logout/", views.logout_view),
]