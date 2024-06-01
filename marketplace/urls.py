"""
URL configuration for yaphets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",LandingPageView,name="landingpage"),
    path("profile/",ProfileView,name="profile"),
    path("address/",AddressView,name="address"),
    path("address/delete/<int:id>",AddressDeleteView,name="addressdelete"),
    path("contact/",ContactUsView,name="contact"),
    path("gallery/",GalleryView,name="gallery"),
    path("painting_for_sale/",PaintingForSaleView,name="painting_for_sale"),
    path("cart/",CartView,name="cart"),
    path('load_paintings/', load_paintings, name='load_paintings'),
    path('load_paintings_filters/', load_paintings_filters, name='load_paintings_filters'),
    path('select_address/', SelectAddressView, name='select_address'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
