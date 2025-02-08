from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login", views.Login.as_view(), name="login"),
    path('sendteste/', views.send, name='sendteste'),
    path('confirm/', views.confirm, name='confirm'),
    path('send/', views.send, name='send'),
    path('history/', views.history, name='history'),
    path('logout/', views.logout_handler, name='logout'),
]
