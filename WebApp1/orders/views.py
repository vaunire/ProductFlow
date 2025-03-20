from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductInstanceForm, ProductInstanceEditForm
from products.models import ProductInstance
from django.db.models import Q

class UserLoanedBooksListView(LoginRequiredMixin, generic.ListView):
    """Отображает список заказов текущего пользователя"""
    model = ProductInstance
    template_name = 'orders/user_loaned_books.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(customer=self.request.user).order_by('due_back')
    
class AllLoanedBooksListView(generic.ListView):
    """Отображает список всех заказов с фильтрацией и поиском"""
    model = ProductInstance
    template_name = 'orders/all_loaned_books.html'
    context_object_name = 'productinstance_list'
    paginate_by = 10  

    def get_queryset(self):
        queryset = ProductInstance.objects.order_by('-due_back')
        
        # Фильтр по статусу
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status__id=status_filter)
        
        # Поиск по колонкам
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(id__icontains=query) |
                Q(product__title__icontains=query) |
                Q(customer__username__icontains=query) |
                Q(customer__first_name__icontains=query) |
                Q(customer__last_name__icontains=query) |
                Q(due_back__icontains=query) |
                Q(status__name__icontains=query)
            )
        
        return queryset

def order_detail_view(request, id):
    """Показывает детали конкретного заказа"""
    order = ProductInstance.objects.get(id=id)
    context = {
        'order': order,
    }
    return render(request, "orders/order_detail.html", context)
    
def order_create_view(request):
    """Создаёт новый заказ через форму"""
    form = ProductInstanceForm()
    success = False
    
    if request.method == "POST":
        form = ProductInstanceForm(request.POST)
        if form.is_valid():
            ProductInstance.objects.create(**form.cleaned_data)
            success = True
            form = ProductInstanceForm() 
    
    context = {
        "form": form,
        "success": success,
    }
    return render(request, "orders/order_create.html", context)

def order_delete_view(request, id):
    """Удаляет заказ и перенаправляет на список всех заказов"""
    order = ProductInstance.objects.get(id=id) 
    order.delete() 
    return redirect('/orders/all-borrowed-books')  

def order_edit_view(request, id):
    """Редактирует существующий заказ через форму"""
    try:
        order = ProductInstance.objects.get(id=id)
        success = False
        
        if request.method == 'POST':
            form = ProductInstanceEditForm(request.POST)
            if form.is_valid():
                for field, value in form.cleaned_data.items():
                    setattr(order, field, value)
                order.save()
                success = True 
        else:
            form = ProductInstanceEditForm(initial={
                'product': order.product,
                'inv_num': order.inv_num,
                'status': order.status,
                'due_back': order.due_back,
                'customer': order.customer,
            })
        
        context = {
            'order': order,
            'form': form,
            'success': success,
        }
        return render(request, "orders/order_edit.html", context)
    except ProductInstance.DoesNotExist:
        return redirect('all-borrowed-books')