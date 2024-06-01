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
import json

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
                return redirect("LandingPageView")
            else:
                print("Incorrect")
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
            user.set_password(password)
            user.save()
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
            return HttpResponse("User with this email does not exist.")

        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"http://example.com/reset-password/{uid.decode('utf-8')}/{token}/"  # Adjust the domain name

        subject = 'Password Reset Request'
        message = f'Please click the link below to reset your password:\n\n{reset_url}'
        from_email = 'duke.ghosh123@gmail.com'  # Make sure this email is configured to send from in your Django settings
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])

    return render(request, "user/forget_password.html", {"site_key": site_key})

def LogoutView(request):
    logout(request)
    return redirect('landingpage')

