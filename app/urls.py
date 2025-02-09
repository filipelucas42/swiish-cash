from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.Login.as_view(), name="login"),
    path('confirm/', views.confirm, name='confirm'),
    path('send-transaction/', views.send_transaction, name='send-transaction'),
    path('send/', views.send, name='send'),
    path('history/', views.history, name='history'),
    path('logout/', views.logout_handler, name='logout'),
    path('verify-code/', views.verify_code, name='verify-code'), 
    path('confirm-otp/', views.confirm_otp, name='confirm-otp'),
    path('confirm-transfer/', views.confirm_transfer, name='confirm-transfer'),
]