from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')

def send(request):
    return render(request, 'app/send.html')

def confirm(request):
    return render(request, 'app/confirm.html')

def withdraw(request):
    return render(request, 'app/withdraw.html')

def history(request):
    return render(request, 'app/history.html')

def page(request):
    return render(request, "app/page1.html")