from django.urls import path
from .views import item_list, checkout_page, product_page
app_name = 'core'
urlpatterns= [
    path('', item_list, name= 'item_list'),
    path('templates/checkout-page.html', checkout_page, name= 'checkout_page'),
    path('templates/product-page.html', product_page, name= 'product_page')
]