from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.conf import settings

from .forms import CustomRegistrationForm

def register_view(request):
    """Обработка регистрации нового пользователя"""
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect(form.cleaned_data.get('next', '/'))  
    else:
        form = CustomRegistrationForm()
    
    context = {
        'form': form,
        'next': request.GET.get('next', '/')
    }
    return render(request, 'registration/register.html', context)