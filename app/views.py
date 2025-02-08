from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login
from app.models import User

class CustomView(View):
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('__method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CustomView, self).dispatch(*args, **kwargs)
    
def index(request):
    response = render(request, 'app/index.html')
    return response

def page(request):
    response = render(request, 'app/page1.html')
    return response

class Login(CustomView):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        try:
            user = User.objects.get(handle=phone_number)
        except ObjectDoesNotExist:
            user = User.objects.create(
                username=phone_number,  # Using phone as username
                handle=phone_number
            )
            user.set_unusable_password()  # Since we're using phone auth
            user.save()
        login(request, user)
        return redirect('index')
