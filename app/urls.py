from django.urls import path

from . import views

urlpatterns = [
    path("page", views.page),
    path("login", views.Login.as_view(), name="login"),
    path("", views.index),
]

