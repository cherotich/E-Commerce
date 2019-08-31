from django.urls import path
from .views import HomeView, checkout_page, ItemDetailView,add_to_cart,remove_from_cart
app_name = 'core'
urlpatterns= [
    path('', HomeView.as_view(), name= 'home_page'),
    path('checkout-page', checkout_page, name= 'checkout_page'),
    path('product-page/<slug>/', ItemDetailView.as_view(), name= 'product_page'),
    path('add-to-cart/<slug>', add_to_cart, name= 'add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name= 'remove-from-cart')
    
]