from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomLoginForm
from .views import *
    
urlpatterns = [
    path('login/', LoginView.as_view(authentication_form = CustomLoginForm), name = 'login'),

    path('register/', register_view, name = 'register'),

    path('logout/', LogoutView.as_view(next_page = '/'), name = 'logout')
]