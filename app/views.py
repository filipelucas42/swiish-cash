from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from app.models import User, Wallet
from app import service

class CustomView(View):
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('__method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CustomView, self).dispatch(*args, **kwargs)
    
def home(request):
    if request.user.is_authenticated:
        wallet = Wallet.objects.get(user=request.user)
        wallet_balance = service.get_balance(wallet.address)
        context = {
            'wallet_balance': wallet_balance
        }
    return render(request, 'app/home.html', context)

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
    
def index(request):
    response = render(request, 'app/index.html')
    return response

def logout_handler(request):
    logout(request)
    return redirect('home')

class Login(CustomView):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        country_code = request.POST.get('country_code')
        full_phone_number = f'{country_code}{phone_number}'
        try:
            user = User.objects.get(handle=full_phone_number)
        except ObjectDoesNotExist:
            wallet_keys = service.create_wallet()
            user = User.objects.create(
                username=full_phone_number,  # Using phone as username
                handle=full_phone_number,
                is_staff=True,
                is_superuser=True,
            )
            wallet = Wallet(
                user=user,
                address=str(wallet_keys["address"]),
                private_key=wallet_keys["private_key"]
            )
            user.set_unusable_password()  # Since we're using phone auth
            user.save()
            wallet.save()
        login(request, user)
        return redirect('home')
    def delete(self, request):
        logout(request)
        return redirect('home')

