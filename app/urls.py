from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login", views.Login.as_view(), name="login"),
    path('send/', views.send, name='send'),
    path('confirm/', views.confirm, name='confirm'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('history/', views.history, name='history'),
]
