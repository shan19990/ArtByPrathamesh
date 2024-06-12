from django.shortcuts import render
from django.http import JsonResponse
from marketplace.models import *

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def sales_chart(request):

    monthwise_sales = {
        'Jan': 1000,
        'Feb': 1200,
        'Mar': 1500,
        'Apr': 1010,
    }

    labels = ['Jan','Feb','Mar','Apr']
    data = [1000,1200,1300,1400]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def gallery(request):
    return render(request, 'dashboard/gallery.html')

def painting_for_sale(request):
    return render(request, 'dashboard/painting_for_sale.html')

def gallery_list(request):
    images = GalleryImagesModel.objects.all()
    print(images)
    return render(request, 'dashboard/gallery_list.html',{"images":images})

def painting_for_sale_list(request):
    return render(request, 'dashboard/painting_for_sale_list.html')

def show_orders(request):
    return render(request, 'dashboard/show_orders.html')

def order(request):
    return render(request, 'dashboard/order.html')

def show_payments(request):
    return render(request, 'dashboard/show_payments.html')

def payment(request):
    return render(request, 'dashboard/payment.html')
