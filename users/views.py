from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from django.urls import reverse, reverse_lazy

from .forms import *


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        '''
        перенаправление при успешной аутонтефикации
        '''
        return reverse_lazy('home')

def login_user(request):
    """заменили классом LogoinView
    """
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            data = forms.cleaned_data
            user = authenticate(request, username=data['login'],
                                password=data['password'])
            if user and user.is_active:
                login(request, user) # авторизация!
                return HttpResponseRedirect(reverse('home'))

    forms = LoginForm()
    return render(request, 'users/login.html', {'form': forms})

def logout_user(request):
    """заменили классом LogoutView
    """
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
