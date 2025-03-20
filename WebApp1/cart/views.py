from django.shortcuts import render, redirect
from products.models import Product
from decimal import Decimal
from .cart import Cart
from django.http import HttpResponseRedirect

def cart_detail(request):
    """Отображает содержимое корзины с общей суммой"""
    cart = Cart(request)
    cart_total = 0
    cart_items = [] 
    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)
        total_price = Decimal(item['price']) * item['quantity']
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': Decimal(item['price']),
            'total_price': total_price,
        })
        cart_total += total_price
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def cart_add(request, product_id):
    """Добавляет продукт в корзину с указанным количеством"""
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        quantity_update = bool(request.POST.get('quantity_update', False))
        cart.add(product=product, quantity=quantity, quantity_update=quantity_update)
    else:
        cart.add(product=product, quantity=1)
    referer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer)

def cart_remove(request, product_id):
    """Удаляет продукт из корзины"""
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.delete(product)
    referer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer)