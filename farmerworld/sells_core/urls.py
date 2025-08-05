from django.urls import path
from core.views import *
from sells_core.views import *

urlpatterns = [
      #seller
  path('seller/add/product/', seller_add_product, name='add_product'),
  path('seller/view/products/', view_products, name='view_products'),
path('seller/view/orders/', view_orders, name='view_orders'),
path('edit/product/<int:product_id>/', edit_product, name='edit_product'),
path('delete/product/<int:product_id>/', delete_product, name='delete_product'),
]