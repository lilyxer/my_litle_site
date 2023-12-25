from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

from .views import *

app_name = 'users'  # namespaces
urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', UserPasswordChange.as_view(), name='change_password'),
    path('change_password_done/', PasswordChangeDoneView.as_view
         (template_name='users/change_password_done.html',
          title='успешно'), name='change_password_done'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', ProfileUser.as_view(), name='profile')
]
