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
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

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
                messages.success(request,"Logged In")
                return redirect("landingpage")
            else:
                messages.error(request,"Username/Password is incorrect")
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
                messages.success(request,"Account Registerd")
            else:
                messages.success(request,"Something went wrong")
            return redirect("userloginemail")

    return render(request, "user/email_register.html",{"site_key":site_key,"error_message":error_message})

def LoginView(request):
    return render(request, "user/login.html")

def ForgetPasswordView(request):
    site_key = RECAPTCHA_PUBLIC_KEY

    if 'form_submitted_expiry' in request.session:
        expiry_time_str = request.session['form_submitted_expiry']
        expiry_time = timezone.make_aware(timezone.datetime.strptime(expiry_time_str, '%Y-%m-%dT%H:%M:%S'))
        
        if timezone.now() >= expiry_time:
            request.session['form_submitted'] = False
            del request.session['form_submitted_expiry']

    if request.method == 'POST':
        if request.session.get('form_submitted', False):
            messages.info(request, "Please wait a while before sending another request")
            return redirect("forgetpassword")
        

        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect("forgetpassword")
        
        username = user.username or email.split('@')[0]

        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"{request.scheme}://{request.get_host()}/user/reset-password/{uid}/{token}/"

        subject = 'Reset Password'
        to_list = [email]  # Send the email to the user who requested the reset
        email_body = f'Hello {username},\n\nPlease click the link below to reset your password:\n{reset_url}\n\nIf you did not request a password reset, please ignore this email.'
        send_mail(subject, email_body, EMAIL_HOST_USER, to_list, fail_silently=True)
        messages.success(request, "Password reset link sent successfully.")
        

        request.session['form_submitted'] = True
        expiry_time = timezone.now() + timezone.timedelta(minutes=30)  # Expires in 30 minutes
        request.session['form_submitted_expiry'] = expiry_time.strftime('%Y-%m-%dT%H:%M:%S')
        request.session.encoder = DjangoJSONEncoder
        return redirect("userlogin")
    

    return render(request, "user/forget_password.html", {"site_key": site_key})

def LogoutView(request):
    logout(request)
    messages.info(request,"Logged Out")
    return redirect('landingpage')


class PasswordResetTokenGeneratorCustom(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )
    

def reset_password_confirm_view(request, uidb64, token):
    if request.method == "POST":
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 == new_password2:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password1)
                user.save()
                messages.success(request, "Password Reset Successful")
                return redirect('userloginemail')
            else:
                messages.error(request, "Something went wrong")
        else:
            messages.error(request, "Passwords do not match")
    
    return render(request, "user/reset_password.html")


