from django.urls import path
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('about/', about, name='about'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:w_slug>', Post.as_view(), name='post'),
    path('category/<slug:c_slug>', Category.as_view(), name='category'),
    path('tags/<slug:t_slug>', Tag.as_view(), name='tag'),
    path('edit/<slug:slug>/', UpdatePost.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', DeletePost.as_view(), name='delete_page'),
]
