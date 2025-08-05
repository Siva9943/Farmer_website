from django.contrib import admin
from django.urls import path
from core.views import *
from sells_core.views import *
urlpatterns = [
  path('', index, name='index'),
  path('home/', home, name='home'),
  #login
  path('login/',login_form,name='login_details'),
  path('seller_login/', seller_login, name='login_info'),
  #signup
  path('signup/', signup, name='signup'),
  path('admin_dashboard/',admin_login,name='admin/'),
  path('seller_dashboard/',seller,name='seller_dashboard'),
  
  path('crop/',crop_view,name='crop'),
  path('crop_details/', upload_crop, name='crop_info'),
  # path('market_update/',market_update,name='market_update'),
  path('crop_view/',crop_view,name='crop_view'),
  path('market-price/', market_price_view, name='market_price'),
  #vegitable data
  path('vegitable_data/', vegitable_data, name='vegitable_data'),

  path('buy-sell/', buy_sell_view, name='buy_sell'),
  path('farming-videos/', farming_videos_view, name='farming_videos'),
  path('government-schemes/', government_schemes_view, name='govt'),
  path('weather/', weather_view, name='weather'),
  path('news/', news_view, name='news'),
  path('community/', community_view, name='command'),
  path('community/comment/<int:post_id>/', add_comment, name='add_comment'),
  path('contact/', contact_view, name='contact'),
  path('feedback/', feedback_view, name='feedback'),  
  path('search/', search_view, name='search'),


  # path('seller/edit/product/<int:product_id>/', edit_product, name='edit_product'),
  # path('seller/delete/product/<int:product_id>/', delete_product, name='delete_product'),
  # path('seller/view/orders/', view_orders, name='view_orders'),
  # path('seller/view/order/<int:order_id>/', view_order_details, name='view_order_details'),
  # path('seller/update/order/<int:order_id>/', update_order_status, name='update_order_status'),
  # path('seller/view/sales/', view_sales, name='view_sales'),
  # path('seller/view/sales/<int:sale_id>/', view_sale_details, name='view_sale_details'),
  # path('seller/update/sale/<int:sale_id>/', update_sale_status, name='update_sale_status'),





  path('logout',logout_user,name='log_out'),
]
