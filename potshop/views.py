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
        
    # if client_id is not None:
    #     request.session.delete('client_id')
    #     client = Client.objects.get(id=client_id)
    # else:
    #     client = Client.objects.create(user=user)
        
        ordered=False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        
        if order.product.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.product.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_item)
        
    return redirect("potshop:product", slug=slug)
    
class CheckoutPageView(TemplateView):
    template_name = "checkout-page.html"