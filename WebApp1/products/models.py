from email.policy import default
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

class Company(models.Model):
    name = models.CharField(max_length = 120, verbose_name = "Наименование компании")
    adress = models.CharField(max_length = 120, verbose_name = "Адрес компании")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length = 120, verbose_name = "Название")
    description = models.TextField(blank = True, null = True, verbose_name = "Описание")
    weight = models.TextField(blank = True, verbose_name = "Вес")
    company = models.ForeignKey(Company, on_delete = models.CASCADE, blank = True, null = True, verbose_name = "Поставщик")
    slug = models.SlugField(max_length = 120, db_index = True, verbose_name = "URL-продукта", allow_unicode = True, null = True, blank = True)
    image = models.ImageField(upload_to = "images", blank = True, verbose_name = "Изображение")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        indexes = [
            models.Index(fields = ['id', 'slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.title, allow_unicode = True)  # Генерируем slug из title
        super().save(*args, **kwargs)

    def short_description(self, max_length = 98):
        if len(self.description) > max_length:
            return f"{self.description[:max_length]}..."
        return self.description
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug]) 

class Status(models.Model):
    name = models.CharField(max_length = 120, verbose_name = "Статус продукта")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name

class ProductInstance(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE, blank = True, null = True)
    inv_num = models.CharField(max_length = 120, verbose_name = "Инвентарный номер")
    status = models.ForeignKey('Status', on_delete = models.CASCADE, blank = True, null = True, verbose_name = "Статус продукта")
    due_back = models.DateField(blank = True, null = True, verbose_name = "Дата окончания статуса продукта")
    customer = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True, verbose_name = "Заказчик")

    class Meta:
        verbose_name = "Экземпляр продукта"
        verbose_name_plural = "Экземпляры продуктов"
        ordering = ['-id']

    def __str__(self):
        return f"{self.inv_num} | {self.product} | {self.status}"

class PriceList(models.Model):
    number = models.IntegerField(verbose_name = "Номер прайс-листа")
    data = models.DateField(verbose_name = "Дата утверждения")
    
    def __str__(self):
        return f"№{self.number} от {self.data}"

    class Meta:
        verbose_name = "Прайс-лист"
        verbose_name_plural = "Прайс-листы"
        ordering = ['number']

class PriceListItem(models.Model):
    number_pricelist = models.ForeignKey('PriceList', on_delete = models.CASCADE, blank = True, null = True, verbose_name = "Номер прайс-листа")
    product_name = models.ForeignKey('Product', on_delete = models.CASCADE, blank = True, null = True, verbose_name = "Название продукта")
    cost_product = models.DecimalField(max_digits = 7, decimal_places = 2, blank = True, null = True, verbose_name = "Цена продукта в прайс-листе")

    def __str__(self):
        return f"{self.product_name} | {self.cost_product} руб."

    class Meta:
        verbose_name = "Позиция прайс-листа"
        verbose_name_plural = "Позиции прайс-листов"
        ordering = ['product_name']
    




