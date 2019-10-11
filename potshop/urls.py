from django.urls import path
from potshop import views
from .views import add_to_cart, remove_from_cart, remove_single_item_from_cart

app_name='potshop'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('store/', views.StorePageView.as_view(), name='store'),
    path('lookbook/', views.BookPageView.as_view(), name='lookbook'),
    path('product/<slug>/', views.productPageView.as_view(), name='product'),
    path('checkout/', views.CheckoutPageView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
]