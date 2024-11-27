from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import (
    login,register,logout,add_to_cart, CartView,add_single_to_cart,remove_single_from_cart,
    HomeView, ProductView, ShopView,BlogView,BlogDetailView,remove_item_from_cart,
    CheckOutView,contactview, aboutview, RefundView
)

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout,name='logout'),
    path('shop/',ShopView.as_view(),name='shop'),
    path('blog/',BlogView.as_view(),name='blog'),
    path('contact/',contactview,name='contact'),
    path('about/',aboutview,name='about'),
    path('cart/',CartView.as_view(),name='cart'),
    path('product/<pk>/',ProductView.as_view(),name='product'),
    path('blog-datail/<pk>/',BlogDetailView.as_view(),name='blog-datail'),
    path('add-to-cart/<pk>/',add_to_cart,name='add-to-cart'),
    path('add-single-to-cart/<pk>/',add_single_to_cart,name='add-single-to-cart'),
    path('remove-single-to-cart/<pk>/',remove_single_from_cart,name='remove-single-from-cart'),
    path('remove-from-cart/<pk>/',remove_item_from_cart,name='remove-from-cart'),
    path('checkout/',CheckOutView.as_view(),name='checkout'),
    path('refund',RefundView.as_view(),name='refund'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)