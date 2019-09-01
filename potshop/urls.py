from django.urls import path
from potshop import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('store/', views.StorePageView.as_view(), name='store'),
    path('lookbook/', views.BookPageView.as_view(), name='lookbook')
]