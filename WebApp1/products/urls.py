from django.urls import path
from .views import *
    
urlpatterns = [ 
    path('', product_list_view, name = 'product_list'), 

    path('create/', product_create_view, name = 'product_create'), 

    path('<int:id>/<slug>/detail', product_detail_view, name = 'product_detail'), 

    path('<int:id>/<slug>/edit/', product_edit_view, name = 'product_edit'),

    path('<int:id>/<slug>/delete/', product_delete_view, name = 'product_delete'), 
]