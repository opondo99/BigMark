from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .models import Product, OrderItem, Order, BillingAddress
from .forms import CheckoutForm

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
    paginate_by = 10
    template_name = "shop.html"
    
    
class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            context = {
                'object':order
            }
            return render(self.request, "order-summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/store")
        
    
class BookPageView(TemplateView):
    template_name = "look-book.html"
    
class productPageView(DetailView):
    model = Product
    template_name = "product-page.html"
    
@login_required  
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
            return redirect("potshop:order-summary")
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_item)
        return redirect("potshop:order-summary")
        
    return redirect("potshop:order-summary")


@login_required  
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
            return redirect("potshop:order-summary")
        else:
            #order does not have this order item
            messages.info(request, "This item was not in your cart")
            return redirect("potshop:product", slug=slug)
    else:
        #the user doesn't have an order
        messages.info(request, "You do not have an active order")
        return redirect("potshop:product", slug=slug)



@login_required  
def remove_single_item_from_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.product.remove(order_item)
            messages.info(request, "This item was updated")
        else:
            #order does not have this order item
            messages.info(request, "This item was not in your cart")
            return redirect("potshop:order-summary")
    else:
        #the user doesn't have an order
        messages.info(request, "You do not have an active order")
        return redirect("potshop:product", slug=slug)
    return redirect("potshop:order-summary")

    
class CheckoutPageView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        
        context = {
            'form' : form
        }
        return render(self.request, "checkout-page.html", context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment = form.cleaned_data.get('apartment')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to the selected payment option
                return redirect('potshop:checkout')
            
            messages.warning(self.request, "Failed checkout")
            return redirect('potshop:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")
        
        
        