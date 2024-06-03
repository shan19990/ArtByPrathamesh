from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from user.models import *
from .models import *
from itertools import chain
from django.http import JsonResponse
from django.core.mail import send_mail
from yaphets.settings import EMAIL_HOST_USER,RECAPTCHA_PUBLIC_KEY
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django import forms
from django.http import JsonResponse
from .models import PaintingForSaleModel
import requests

# Create your views here.
def LandingPageView(request):
    images = GalleryImagesModel.objects.order_by('?')
    return render(request, "marketplace/landingpage.html",{"images":images,'username': request.user.username})

def CartView(request):
    return render(request,"marketplace/cart.html",{'username': request.user.username})

def SelectAddressView(request):
    user = request.user
    addresses = AddressModel.objects.filter(user=user)
    return render(request,"marketplace/cart_address.html",{"addresses":addresses})

def ProfileView(request):
    if request.method == "POST":
        form = forms.Form(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Profile Update Successfully")
            return redirect('profile')
        else:
            messages.error(request, "Something went wrong")
            return redirect('profile')

    
    # Return HTML template if not a POST request
    return render(request, "marketplace/profile.html", {'username': request.user.username})

def AddressView(request):
    user = request.user
    addresses = AddressModel.objects.filter(user=user)
    if request.method == "POST":
        form = forms.Form(request.POST)
        if form.is_valid():
            street = request.POST.get('street')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            phone_number = request.POST.get('phone_number')
            id = request.POST.get('form')
            if id == "":
                address = AddressModel.objects.create(user=request.user, street_address=street, city=city, state=state, pincode=postal_code, contact=phone_number)
                if address is not None:
                    messages.success(request, "Address Added")
                else:
                    messages.error(request, "Error Adding Address")
            else:
                address = AddressModel.objects.get(pk=id)
                address.street_address = street
                address.city = city
                address.state = state
                address.pincode = postal_code
                address.contact = phone_number
                address.save()
                if address is not None:
                    messages.success(request, "Address Edited")
                else:
                    messages.error(request, "Error Editing Address")
    return render(request,"marketplace/address.html",{"addresses":addresses,'username': request.user.username})

def AddressDeleteView(request, id):
    try:
        address = AddressModel.objects.get(pk=id)
        address.delete()
        messages.info(request, "Address Deleted")
    except AddressModel.DoesNotExist:
        messages.error(request, "Address does not exist")
    return redirect("address")


def ContactUsView(request):
    site_key = RECAPTCHA_PUBLIC_KEY
    
    if 'form_submitted_expiry' in request.session:
        expiry_time_str = request.session['form_submitted_expiry']
        expiry_time = timezone.make_aware(timezone.datetime.strptime(expiry_time_str, '%Y-%m-%dT%H:%M:%S'))
        
        if timezone.now() >= expiry_time:
            request.session['form_submitted'] = False
            del request.session['form_submitted_expiry']

    if request.method == "POST":
        if request.session.get('form_submitted', False):
            messages.info(request, "Please wait a while before sending another request")
            return redirect("contact")
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        email_body = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Message: {message}
        """

        subject = 'Contact Form'
        to_list = [EMAIL_HOST_USER]
        send_mail(subject, email_body, EMAIL_HOST_USER, to_list, fail_silently=True)
        messages.success(request, "Your enquiry has been sent to us. We will get back to you soon")
        
        request.session['form_submitted'] = True
        expiry_time = timezone.now() + timezone.timedelta(minutes=30)  # Expires in 30 minutes
        request.session['form_submitted_expiry'] = expiry_time.strftime('%Y-%m-%dT%H:%M:%S')
        request.session.encoder = DjangoJSONEncoder

    return render(request, "marketplace/contactus.html", {'username': request.user.username, "site_key":site_key})


def GalleryView(request):
    query = PaintingForSaleModel.objects.order_by('?')
    images = list(chain.from_iterable([query] * 3))
    return render(request,"marketplace/gallery.html",{'username': request.user.username})

def PaintingForSaleView(request):
    return render(request,"marketplace/painting_for_sale.html",{'username': request.user.username})

def get_user_country(request):
    # Get the user's IP address from the request
    ip = request.META.get('REMOTE_ADDR')
    # Use a geolocation API to get the user's country
    response = requests.get(f'http://ipinfo.io/{ip}/json')
    data = response.json()
    return data.get('country')

def adjust_cost_by_country(cost, country):
    # Implement your logic for adjusting the cost based on the country
    if country == 'US':
        return cost * 1.1  # For example, 10% increase for US
    elif country == 'IN':
        return cost * 10.0  # For example, 10% discount for India
    # Add more conditions as needed
    return cost

def load_paintings(request):
    country = get_user_country(request)
    print(country)
    page = request.GET.get('page', 1)
    paintings_per_page = 5
    start_index = (int(page) - 1) * paintings_per_page
    end_index = start_index + paintings_per_page
    paintings = PaintingForSaleModel.objects.all()[start_index:end_index]
    
    data = []
    for painting in paintings:
        adjusted_cost = adjust_cost_by_country(painting.cost, country)
        data.append({
            'id': painting.id,
            'title': painting.title,
            'description': painting.description,
            'cost': adjusted_cost,
            'image_url': painting.image.url
        })
    
    return JsonResponse({'paintings': data})

def load_paintings_filters(request):
    # Get filter parameters from request
    style_filter = request.GET.get('style')
    sort_option = request.GET.get('sort_option')

    print(style_filter,sort_option)

    # Filter paintings based on parameters
    paintings = PaintingForSaleModel.objects.all()

    if style_filter:
        if style_filter != "all":
            paintings = paintings.filter(type=style_filter)

    # Apply sorting based on sort_option
    if sort_option == 'price-high-low':
        paintings = paintings.order_by('-cost')
    elif sort_option == 'price-low-high':
        paintings = paintings.order_by('cost')
    elif sort_option == 'size-low-high':
        paintings = paintings.order_by('height', 'width')
    elif sort_option == 'size-high-low':
        paintings = paintings.order_by('-height', '-width')

    # Assuming you want to return 12 paintings per page
    paintings_per_page = 12

    # Get the page number from the request, default to 1 if not provided
    page = int(request.GET.get('page', 1))
    start_index = (page - 1) * paintings_per_page
    end_index = start_index + paintings_per_page

    # Slice the queryset to get the paintings for the current page
    paintings_for_page = paintings[start_index:end_index]

    # Serialize paintings data
    data = [{'id': painting.id, 'title': painting.title, 'description': painting.description, 'cost': painting.cost, 'image_url': painting.image.url, 'type': painting.type, 'height': painting.height, 'width': painting.width} for painting in paintings_for_page]

    return JsonResponse({'paintings': data})
