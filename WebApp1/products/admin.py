from django.contrib import admin
from django.db.models import Count
from .models import Product, Company, ProductInstance, Status, PriceList, PriceListItem

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_short_description', 'weight', 'company', 'show_count')
    list_filter = ('company',)
    inlines = [ProductInstanceInline]
    search_fields = ('title',)

    def get_short_description(self, obj):
        return obj.short_description()
    get_short_description.short_description = 'Описание'

    def show_count(self, obj):
        """ Возвращает количество заказов для данного продукта """
        result = ProductInstance.objects.filter(product = obj).aggregate(Count('product'))
        return result['product__count']
    show_count.short_description = 'Заказано, шт'
admin.site.register(Product, ProductAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'adress')
    search_fields = ('name',)
admin.site.register(Company, CompanyAdmin)

class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('inv_num', 'product', 'status')
    list_filter = ('product', 'status')
    fieldsets = (
        (
            'Заказанный продукт',
            {
                'fields': ('inv_num', 'product')
            },
        ),
        (
            'Статус и окончание его действия',
            {
                'fields': ('customer', 'status', 'due_back')
            },
        ),
    )
admin.site.register(ProductInstance, ProductInstanceAdmin)

admin.site.register(Status)
admin.site.register(PriceList)
admin.site.register(PriceListItem)


