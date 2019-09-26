from django.urls import path
from potshop import views
from .views import add_to_cart
# from django.urls import reverse

# from django.core.urlresolvers import reverse


app_name='potshop'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('store/', views.StorePageView.as_view(), name='store'),
    path('lookbook/', views.BookPageView.as_view(), name='lookbook'),
    path('product/<slug>/', views.productPageView.as_view(), name='product'),
    path('checkout/', views.CheckoutPageView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
]

# reverse('home')
