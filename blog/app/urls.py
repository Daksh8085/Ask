from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.signin, name="signin"),
    path("logout/", views.signout, name="signout"),
    path("signup/", views.signup, name="signup"),
]
