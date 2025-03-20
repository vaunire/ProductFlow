from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from .models import Product, Company, ProductInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm, ProductEditForm
from django.db.models import Q
from cart.cart import Cart 

def index_view(request):
    """Отображает главную страницу с общей статистикой продуктов и компаний"""
    num_product = Product.objects.all().count()
    num_company = Company.objects.all().count()
    num_instance = ProductInstance.objects.all().count()
    num_instance_available = ProductInstance.objects.filter(status_id__exact=2).count()
    context = {
        'num_product': num_product,
        'num_company': num_company,
        'num_instance': num_instance,
        'num_instance_available': num_instance_available,
    }
    return render(request, "pages/home.html", context)

def product_list_view(request):
    """Выводит список продуктов с поддержкой поиска"""
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(weight__icontains=query)
        )
    context = {
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

def product_detail_view(request, id, slug):
    """Показывает детали конкретного продукта или перенаправляет на список"""
    try:
        product = Product.objects.get(id=id, slug=slug)
        context = {
            "product": product,
        }
        return render(request, "products/product_detail.html", context)
    except Product.DoesNotExist:
        return redirect('product_list')

def product_create_view(request):
    """Создаёт новый продукт через форму"""
    form = ProductForm()
    success = False
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # request.FILES для обработки изображения
        if form.is_valid():
            product = Product.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                weight=form.cleaned_data['weight'],
                slug=form.cleaned_data['slug'], 
                image=form.cleaned_data['image'] 
            )
            success = True
            form = ProductForm() 
    context = {
        "form": form,
        "success": success,
    }
    return render(request, "products/product_create.html", context)

def product_delete_view(request, id, slug):
    """Удаляет продукт и перенаправляет на список"""
    try:
        product = Product.objects.get(id=id, slug=slug)
        product.delete()
        return redirect('product_list')
    except Product.DoesNotExist:
        return redirect('product_list')

def product_edit_view(request, id, slug):
    """Редактирует существующий продукт через форму"""
    try:
        product = Product.objects.get(id=id, slug=slug)
        success = False
        if request.method == 'POST':
            form = ProductEditForm(request.POST, request.FILES)  # request.FILES для обработки изображения
            if form.is_valid():
                product.title = form.cleaned_data['title']
                product.description = form.cleaned_data['description']
                product.weight = form.cleaned_data['weight']
                product.slug = form.cleaned_data['slug'] 
                if form.cleaned_data['image']: 
                    product.image = form.cleaned_data['image']
                product.save()  
                success = True
        else:
            form = ProductEditForm(initial={
                'title': product.title,
                'description': product.description,
                'weight': product.weight,
                'slug': product.slug,  
            })
        context = {
            'product': product,
            'form': form,
            'success': success,
        }
        return render(request, "products/product_edit.html", context)
    except Product.DoesNotExist:
        return redirect('product_list')

class CompanyListView(generic.ListView):
    """Отображает список всех компаний"""
    model = Company
    template_name = 'companies/company_list.html'
    context_object_name = 'company_list'