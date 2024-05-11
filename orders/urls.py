from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('delete_cart/<int:product_id>/', views.DeleteCartView.as_view(), name='cart_delete'),
    path('apply/<int:order_id>/', views.CouponApplyView.as_view(), name='apply_coupon'),
]
