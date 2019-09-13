from django.urls import path
from .views import HomeView, checkout_page,remove_from_cart_trash, add_to_cart_single,ItemDetailView,add_to_cart,remove_from_cart,OrderSummaryView,remove_single_item_from_cart
app_name = 'core'
urlpatterns= [
    path('', HomeView.as_view(), name= 'home_page'),
    path('checkout-page', checkout_page, name= 'checkout_page'),
    path('order_summary', OrderSummaryView.as_view(), name= 'order-summary'),
    path('product-page/<slug>/', ItemDetailView.as_view(), name= 'product_page'),
    path('add-to-cart/<slug>', add_to_cart, name= 'add-to-cart'),
    path('add-to-cart-single/<slug>', add_to_cart_single, name= 'add-to-cart-single'),  
    path('remove-from-cart/<slug>', remove_from_cart, name= 'remove-from-cart'),
    path('remove-from-cart-trash/<slug>', remove_from_cart_trash, name= 'remove-from-cart-trash'),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart, name= 'remove-single-item-from-cart')
    
]