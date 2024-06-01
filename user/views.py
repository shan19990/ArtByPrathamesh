from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.conf import settings
from django.http import HttpResponse
import requests
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from yaphets.settings import EMAIL_HOST_USER,RECAPTCHA_PUBLIC_KEY
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

def LoginEmailView(request):
    site_key = settings.RECAPTCHA_PUBLIC_KEY
    captcha_error = ""
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = settings.RECAPTCHA_PRIVATE_KEY
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', {
            'secret': secret_key,
            'response': recaptcha_response
        })
        data = response.json()
        if data['success']:
            email = request.POST.get('email')
            password = request.POST.get('password')
            username = email.split('@')[0]
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success("Logged In")
                return redirect("LandingPageView")
            else:
                messages.success("Username/Password is incorrect")
        else:
            captcha_error = 'reCAPTCHA verification failed. Please complete the CAPTCHA.'

    return render(request, "user/email_login.html",{"site_key":site_key,"captcha_error":captcha_error})

def RegisterEmailView(request):
    site_key = settings.RECAPTCHA_PUBLIC_KEY
    error_message = ""
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = settings.RECAPTCHA_PRIVATE_KEY
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', {
            'secret': secret_key,
            'response': recaptcha_response
        })
        data = response.json()
        if data['success']:
            email = request.POST.get('email')
            password = request.POST.get('password')
            username = email.split('@')[0]
            user = User.objects.create(username=username,email=email)
            if user is not None:
                user.set_password(password)
                user.save()
                messages.success("Account Registerd")
            else:
                messages.success("Something went wrong")
            return redirect("userloginemail")

    return render(request, "user/email_register.html",{"site_key":site_key,"error_message":error_message})

def LoginView(request):
    return render(request, "user/login.html")

def ForgetPasswordView(request):
    site_key = settings.RECAPTCHA_PUBLIC_KEY
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect("forgetpassword")

        token_generator = PasswordResetTokenGeneratorCustom()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{uid.decode('utf-8')}/{token}/"

        subject = 'Contact Form'
        to_list = [EMAIL_HOST_USER]
        email_body = 'Please click the link below to reset your password'
        send_mail(subject, email_body, EMAIL_HOST_USER, to_list, fail_silently=True)

        messages.success(request, "Password reset link sent successfully.")

    return render(request, "user/forget_password.html", {"site_key": site_key})

def LogoutView(request):
    logout(request)
    messages.warning(request,"Logged Out")
    return redirect('landingpage')


class PasswordResetTokenGeneratorCustom(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )