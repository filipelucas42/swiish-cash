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
        return redirect('send')
    return render(request, 'app/home.html')

def sendtest(request):
    return render(request, 'app/sendtest.html')

def send_transaction(request):
    user = request.user
    value = request.POST.get('value')
    phone_number = request.POST.get('phone_number')

    wallet_from = Wallet.objects.get(user=user)
    wallet_to = Wallet.objects.get(user__handle=phone_number)
    service.send_transaction(wallet_from.address, wallet_to.address, value, wallet_from.private_key)
    return redirect('send')

def confirm(request):
    user = request.user
    value = request.POST.get('value')
    phone_number = request.POST.get('phone_number')
    country_code = request.POST.get('country_code')
    full_phone_number = f'{country_code}{phone_number}'
    
    try:
        user_to_send = User.objects.get(handle=full_phone_number)
    except ObjectDoesNotExist:
        user_to_send = service.create_user(full_phone_number)
    wallet_from = Wallet.objects.get(user=user)
    wallet_to = Wallet.objects.get(user=user_to_send)
    gas_estimate = service.estimate_gas_for_transfer(wallet_from.address, wallet_to.address, value)
    context = {}
    context["value"] = value
    context["gas"] = gas_estimate["total_cost_avax"]
    context["recipient"] = full_phone_number
    return render(request, 'app/confirm.html', context)

def send(request):
    context = {}
    country_list = [
        ("+1", "US"), ("+351", "PT"), ("+44", "GB"), ("+55", "BR"),
        ("+33", "FR"), ("+49", "DE"), ("+81", "JP"), ("+91", "IN"),
        ("+61", "AU"), ("+86", "CN"), ("+34", "ES"), ("+7", "RU"),
        ("+39", "IT"), ("+82", "KR"), ("+90", "TR"), ("+964", "IQ"),
    ]
    
    context["country_list"] = country_list
        
    if request.user.is_authenticated:
        wallet = Wallet.objects.get(user=request.user)
        wallet_balance = service.get_balance(wallet.address)
        context["wallet_balance"] =  wallet_balance
    return render(request, 'app/send.html', context)

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
            user = service.create_user(full_phone_number)
        login(request, user)
        return redirect('send')
    def delete(self, request):
        logout(request)
        return redirect('home')

