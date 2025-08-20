from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy/<int:product_id>/', views.buy, name='buy'),
    path('purchases/', views.purchases, name='purchases'),
    path('orders/', views.orders_view, name='orders'),
    path('profile/', views.profile, name='profile'),
    path('checkout/', views.checkout, name='checkout'),
    path('products/', views.home, name='products'),
]