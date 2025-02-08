from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    response = render(request, 'app/index.html')
    return response

def page(request):
    response = render(request, 'app/page1.html')
    return response
