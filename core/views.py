from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView,View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(ListView):
    model=Item
    paginate_by = 10 #saved already
    template_name="home-page.html"
class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not an active order")
            return redirect("/")
        
  
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
@login_required
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

@login_required
def remove_from_cart(request, slug):
    item= get_object_or_404(Item, slug=slug)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter( item=item, user=request.user, ordered=False )[0]
            order.items.remove(order_item)
            order_item.quantity =1
            order_item.save()
            messages.info(request, "This item was removed from your cart")
            return redirect("core:product_page", slug=slug) 
            
    
        else:

            messages.info(request, "This item was not in your cart")
            #the order does not contain this item
            return redirect("core:product_page", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product_page", slug=slug)
        #add a message that the user does not have an order

@login_required
def remove_from_cart_trash(request, slug):
    item= get_object_or_404(Item, slug=slug)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter( item=item, user=request.user, ordered=False )[0]
            order.items.remove(order_item)
            order_item.quantity =1
            order_item.save()
            
            messages.info(request, "This item was removed from your cart")
            return redirect("core:order-summary") 
            
    
        else:

            messages.info(request, "This item was not in your cart")
            #the order does not contain this item
            return redirect("core:order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:order-summary", slug=slug)
        #add a message that the user does not have an order

@login_required
def add_to_cart_single(request, slug):
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
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect("core:order-summary")

        
@login_required
def remove_single_item_from_cart(request, slug):
    item= get_object_or_404(Item, slug=slug)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter( item=item, user=request.user, ordered=False )[0]
            order_item.quantity -=1
            order_item.save()
            messages.info(request, "Quantity was updated") 
            return redirect("core:order-summary")
      
        else:
            messages.info(request, "This item was not in your cart")
            #the order does not contain this item
            return redirect("core:order-summary",slug=slug)
     
    else:
        
        messages.info(request, "You do not have an active order")
        return redirect("core:product_page", slug=slug)
        #add a message that the user does not have an order 

