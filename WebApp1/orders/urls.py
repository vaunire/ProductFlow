from django.urls import path
from .views import *

urlpatterns = [ 
    path('my-borrowed-books/', UserLoanedBooksListView.as_view(), name = 'my_borrowed_books'),  

    path('all-borrowed-books/', AllLoanedBooksListView.as_view(), name = 'all_borrowed_books'), 

    path('create/', order_create_view, name = 'order_create'),

    path('<int:id>/detail/', order_detail_view, name = 'order_detail'),

    path('<int:id>/edit/', order_edit_view, name = 'order_edit'),

    path('<int:id>/delete/', order_delete_view, name = 'order_delete'),
]