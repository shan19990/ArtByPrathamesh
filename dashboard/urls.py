from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("",dashboard,name="dashboard"),
    path('sales_chart/', sales_chart, name='sales-chart'),
    path("gallery_list/",gallery_list,name="dashboard_gallery_list"),
    path("gallery_edit/<int:item_id>/",gallery_edit,name="dashboard_gallery_image_edit"),
    path("gallery_image_delete/<int:item_id>/",gallery_image_delete,name="dashboard_gallery_image_delete"),
    path("painting_for_sale_list/",painting_for_sale_list,name="dashboard_painting_for_sale_list"),
    path("painting_for_sale_delete/<int:item_id>/",painting_for_sale_delete,name="dashboard_painting_for_sale_delete"),
    path("painting_for_sale_edit/<int:item_id>/",painting_for_sale_edit,name="dashboard_painting_for_sale_edit"),
    path("user/",user_panel,name="user_panel"),
    path("user_edit/<int:user_id>/",user_edit,name="user_edit"),
    path("show_orders/",show_orders,name="show_orders"),
    path("order/",order,name="order"),
    path("payment/",payment,name="payment"),
    path("show_payments/",show_payments,name="show_payments"),
]
