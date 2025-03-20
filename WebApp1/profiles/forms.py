from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Модуль используется для проверки полей на соответствие определённому формату
import re

# Блок для формы логина
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Проверяем, существует ли пользователь
            if not User.objects.filter(username=username).exists():
                raise ValidationError(f"Пользователь {username} не найден в системе.")
            
            # Проверяем пароль
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Неверный пароль, попробуйте еще раз")
            
            # Если всё ок, сохраняем пользователя для авторизации
            self.user_cache = user

        return self.cleaned_data

# Блок для формы регистрации
class CustomRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False 
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False 
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=False 
    )
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Проверка на английские символы и разрешённые знаки
        if not re.match(r'^[a-zA-Z0-9@.+-_]+$', username):
            raise ValidationError("Имя пользователя должно содержать только английские буквы, цифры и некоторые символы")
        # Проверка на запрещённые символы
        if any(char in username for char in '<> /\\|&%#'):
            raise ValidationError("Имя пользователя содержит запрещённые символы")
        # Проверка уникальности
        if User.objects.filter(username=username).exists():
            raise ValidationError("Это имя пользователя уже занято")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован")
        return email or None

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        # Проверка совпадения паролей
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email'] or ''
        if commit:
            user.save()
        return user