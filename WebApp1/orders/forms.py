from django import forms
from products.models import ProductInstance, Product, Status
from django.contrib.auth.models import User
from datetime import date

# Кастомный ModelChoiceField с поддержкой label_from_instance
class CustomModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, label_from_instance=None, **kwargs):
        self.label_from_instance = label_from_instance
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        if self.label_from_instance:
            return self.label_from_instance(obj)
        return super().label_from_instance(obj)

# Функция для форматирования отображения пользователя
def user_label_from_instance(user):
    full_name = user.get_full_name() 
    return f"{full_name} | {user.username}" if full_name else user.username

# Форма для создания заказа
class ProductInstanceForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=True,
        label="Продукт *",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    inv_num = forms.CharField(
        required=True,
        label="Инвентарный номер *",
        widget=forms.TextInput(attrs={"placeholder": "Введите инвентарный номер"})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label="Статус *",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    due_back = forms.DateField(
        required=False,
        label="Дата окончания статуса",
        widget=forms.DateInput(attrs={"type": "date", "placeholder": "Выберите дату"})
    )
    customer = CustomModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="Заказчик *",
        widget=forms.Select(attrs={"class": "form-control"}),
        label_from_instance=user_label_from_instance  # Кастомное отображение
    )

    def clean_due_back(self):
        due_back = self.cleaned_data.get('due_back')
        if due_back:
            if due_back < date.today():
                raise forms.ValidationError("Дата окончания не может быть раньше сегодняшнего дня.")
        return due_back

# Форма для редактирования заказа
class ProductInstanceEditForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=True,
        label="Продукт *",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    inv_num = forms.CharField(
        required=True,
        label="Инвентарный номер *",
        widget=forms.TextInput(attrs={"placeholder": "Введите новый инвентарный номер"})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label="Статус *",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    due_back = forms.DateField(
        required=False,
        label="Дата окончания статуса",
        widget=forms.DateInput(attrs={"type": "date", "placeholder": "Выберите новую дату"})
    )
    customer = CustomModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="Заказчик *",
        widget=forms.Select(attrs={"class": "form-control"}),
        label_from_instance=user_label_from_instance
    )

    def clean_due_back(self):
        due_back = self.cleaned_data.get('due_back')
        if due_back:
            if due_back < date.today():
                raise forms.ValidationError("Дата окончания не может быть раньше сегодняшнего дня.")
        return due_back