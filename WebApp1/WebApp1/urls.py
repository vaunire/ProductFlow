from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from products.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('pages/', include('pages.urls')),  

    path('orders/', include('orders.urls')),  

    path('products/', include('products.urls')),  

    path('accounts/', include('profiles.urls')), 

    path('cart/', include('cart.urls')), 

    path('', index_view, name = 'home'),

    path('companies/', CompanyListView.as_view(), name = 'company_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)