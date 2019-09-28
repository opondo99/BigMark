from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
from .models import Product, OrderItem, Order

# Create your views here.
# def item_list(request):
#     context = {
#         'items': Product.object.all()
#     }
#     return render(request, "item_list.html", context)

class HomePageView(TemplateView):
    template_name = "home.html"
    
class AboutPageView(TemplateView):
    template_name = "about.html"
    
class StorePageView(ListView):
    model = Product
    template_name = "shop.html"
    
class BookPageView(TemplateView):
    template_name = "look-book.html"
    
class productPageView(DetailView):
    model = Product
    template_name = "product-page.html"
    
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
        )
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        
        if order.product.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item was added to your cart")
            
        else:
            
            order.product.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("potshop:product", slug=slug)
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_item)
        return redirect("potshop:product", slug=slug)
        
    return redirect("potshop:product", slug=slug)

def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        
        if order.product.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.product.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            #order does not have this order item
            messages.info(request, "This item was not in your cart")
            return redirect("potshop:product", slug=slug)
    else:
        #the user doesn't have an order
        messages.info(request, "You do not have an active order")
        return redirect("potshop:product", slug=slug)
    return redirect("potshop:product", slug=slug)

    
class CheckoutPageView(TemplateView):
    template_name = "checkout-page.html"
    