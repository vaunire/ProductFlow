from decimal import Decimal
from django.conf import settings
from products.models import Product, PriceListItem

class Cart(object):
    def __init__(self, request):
        """Инициализируем корзину"""
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        # Используем уникальный ключ для корзины: для авторизованных — 'cart_<user_id>', для анонимов — CART_SESSION_ID
        self.cart_key = f'cart_{self.user.id}' if self.user else settings.CART_SESSION_ID
        cart = self.session.get(self.cart_key)
        if not cart:
            # Если корзины нет, создаём пустую и сохраняем в сессии
            cart = self.session[self.cart_key] = {}
        self.cart = cart

    def add(self, product, quantity=1, quantity_update=False):
        """Добавление товара в корзину и/или обновление его количества"""
        # Ищем последний PriceListItem для данного продукта
        price_item = PriceListItem.objects.filter(product_name=product).last()
        if not price_item:
            raise ValueError(f'Для продукта {product.title} цена в прайс-листе не указана')
        
        product_id = str(product.id)
        if product_id not in self.cart:
            # Если товара нет в корзине, добавляем его с начальным количеством 0 и ценой из прайс-листа
            self.cart[product_id] = {'quantity': 0, 'price': str(price_item.cost_product)}
        
        if quantity_update:
            # Если обновляем количество, устанавливаем новое значение
            self.cart[product_id]['quantity'] = quantity
        else:
            # Иначе увеличиваем количество на указанное значение
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def __len__(self):
        """Подсчёт общего количества товаров в корзине"""
        # Суммируем количество всех товаров в корзине
        return sum(item['quantity'] for item in self.cart.values())

    def delete(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            # Если товар есть в корзине, удаляем его и сохраняем изменения
            del self.cart[product_id]
            self.save()

    def save(self):
        """Сохранение корзины в сессии"""
        # Сохраняем корзину в сессии под уникальным ключом и отмечаем сессию как изменённую
        self.session[self.cart_key] = self.cart
        self.session.modified = True