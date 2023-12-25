from django.db.models.base import Model as Model
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.urls import reverse, reverse_lazy

from .forms import *


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     '''
    #     перенаправление при успешной аутонтефикации
    #     '''
    #     return reverse_lazy('home')


class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль'}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])
    
    def get_object(self, queryset=None):
        return self.request.user

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html', 
                          {'title': 'добро пожаловать!'})
    form = RegisterUserForm()
    return render(request, 'users/register.html', 
                  {'form': form, 'title': 'Регистрация'})


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
