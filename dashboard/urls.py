from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("",dashboard,name="dashboard"),
    path('sales_chart/', sales_chart, name='sales-chart'),
    path("gallery_add/",gallery,name="dashboard_gallery"),
    path("painting_for_sale/",painting_for_sale,name="dashboard_painting_for_sale"),
    path("gallery_list/",gallery_list,name="dashboard_gallery_list"),
    path("painting_for_sale_list/",painting_for_sale_list,name="dashboard_painting_for_sale_list"),
    path("show_orders/",show_orders,name="show_orders"),
    path("order/",order,name="order"),
    path("payment/",payment,name="payment"),
    path("show_payments/",show_payments,name="show_payments"),
]
