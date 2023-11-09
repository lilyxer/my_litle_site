from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import *

def login_user(request):
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            data = forms.cleaned_data
            user = authenticate(request, username=data['login'],
                                password=data['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

    forms = LoginForm()
    return render(request, 'users/login.html', {'form': forms})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
