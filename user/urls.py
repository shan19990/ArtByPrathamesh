from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("login/",LoginView,name="userlogin"),
    path("logout/",LogoutView,name="userlogout"),
    path("email/login/",LoginEmailView,name="userloginemail"),
    path("email/register/",RegisterEmailView,name="userregisteremail"),
    path("forgetpassword/",ForgetPasswordView,name="forgetpassword"),
    path('reset-password/<uidb64>/<token>/', reset_password_confirm_view, name='reset_password_confirm'),
]
