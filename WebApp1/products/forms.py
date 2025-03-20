from django import forms
from .models import Product

# Форма создания продукта
class ProductForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="Название",
        widget=forms.TextInput(attrs={"placeholder": "Наименование продукта"})
    )
    description = forms.CharField(
        required=False,
        label="Описание",
        widget=forms.Textarea(attrs={
            "placeholder": "Описание для продукта",
            "rows": 5,
            "cols": 25,
        })
    )
    weight = forms.CharField(
        required=False,
        label="Вес, г"
    )
    slug = forms.SlugField( 
        required=False,
        label="URL - продукта",
        widget=forms.TextInput(attrs={"placeholder": "URL (оставьте пустым для автогенерации)"})
    )
    image = forms.ImageField( 
        required=False,
        label="Изображение",
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight:
            try:
                weight_value = float(weight)
                if weight_value < 0:
                    raise forms.ValidationError("Вес не может быть отрицательным.")
                return weight
            except ValueError:
                raise forms.ValidationError("Введите корректное число для веса.")
        return weight

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slug.lower()
        return slug


# Форма редактирования продукта
class ProductEditForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="Новое название",
        widget=forms.TextInput(attrs={"placeholder": "Новое наименование продукта"})
    )
    description = forms.CharField(
        required=False,
        label="Новое описание",
        widget=forms.Textarea(attrs={
            "placeholder": "Новое описание для продукта",
            "rows": 5,
            "cols": 25,
        })
    )
    weight = forms.CharField(
        required=False,
        label="Новый вес, г"
    )
    slug = forms.SlugField(  
        required=False,
        label="Новый URL - продукта",
        widget=forms.TextInput(attrs={"placeholder": "Новый URL (оставьте пустым для автогенерации)"})
    )
    image = forms.ImageField(  
        required=False,
        label="Новое изображение",
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight:
            try:
                weight_value = float(weight)
                if weight_value < 0:
                    raise forms.ValidationError("Вес не может быть отрицательным.")
                return weight
            except ValueError:
                raise forms.ValidationError("Введите корректное число для веса.")
        return weight

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slug.lower() 
        return slug