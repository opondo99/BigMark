from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"
    
class AboutPageView(TemplateView):
    template_name = "about.html"
    
class StorePageView(TemplateView):
    template_name = "shop.html"
    
class BookPageView(TemplateView):
    template_name = "look-book.html"