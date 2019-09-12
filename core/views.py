from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages

class HomeView(ListView):
    model=Item
    paginate_by = 10
    template_name="home-page.html"
class ItemDetailView(DetailView):
    model=Item 
    template_name="product-page.html" 
      

# def product_page(request):
#     context={
#         'items':Item.objects.all()
#     }
#     return render(request, "product-page.html", context)
def checkout_page(request):
    return render(request, "checkout-page.html")

def add_to_cart(request, slug):
    item= get_object_or_404(Item, slug=slug)
    order_item, created= OrderItem.objects.get_or_create( item=item, user=request.user, ordered=False )
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:product_page", slug=slug)
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("core:product_page", slug=slug)
    else:
        ordered_date = timezone.now()
        Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect("core:product_page", slug=slug)

def remove_from_cart(request, slug):
    item= get_object_or_404(Item, slug=slug)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter( item=item, user=request.user, ordered=False )[0]
            order.items.remove(order_item) 
            messages.info(request, "This item was removed from your cart") 
        else:
            messages.info(request, "This item was not in your cart")
            #the order does not contain this item
            return redirect("core:product_page", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product_page", slug=slug)
        #add a message that the user does not have an order
    

    

