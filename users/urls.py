from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

app_name = 'users'  # namespaces
urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
