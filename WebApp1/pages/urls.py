from django.urls import path
from .views import *

urlpatterns = [ 
    path('contact/', contact_view, name = 'contact'),

    path('about/', about_view, name = 'about'),  
    
    path('social/', social_view, name = 'social'),  
]