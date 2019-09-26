from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product

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
    
class CheckoutPageView(TemplateView):
    template_name = "checkout-page.html"