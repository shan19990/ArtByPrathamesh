from django.shortcuts import render, redirect, get_object_or_404
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


def gallery_edit(request, item_id):
    gallery_item = get_object_or_404(GalleryImagesModel, id=item_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES.get('image')
        
        if title:
            gallery_item.title = title
        if image_file:
            gallery_item.image = image_file
        gallery_item.save()
        return redirect("dashboard_gallery_list")
    return render(request, 'dashboard/gallery_edit.html', {"gallery_item": gallery_item})


def painting_for_sale(request):
    return render(request, 'dashboard/painting_for_sale.html')

def gallery_list(request):
    gallery_items = GalleryImagesModel.objects.all().order_by('-id')
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES.get('image')
        print(title,image_file)
        if title and image_file:
            new_image = GalleryImagesModel(title=title, image=image_file)
            new_image.save()
    return render(request, 'dashboard/gallery_list.html',{"gallery_items":gallery_items})

def gallery_image_delete(request, item_id):
    item = get_object_or_404(GalleryImagesModel, pk=item_id)
    item.delete()
    return redirect('dashboard_gallery_list')

def painting_for_sale_delete(request, item_id):
    item = get_object_or_404(PaintingForSaleModel, pk=item_id)
    item.delete()
    return redirect('dashboard_painting_for_sale_list')

def painting_for_sale_edit(request, item_id):
    gallery_item = get_object_or_404(PaintingForSaleModel, id=item_id)
    print("Title:", gallery_item.title)
    print("Description:", gallery_item.description)
    print("Height:", gallery_item.height)
    print("Width:", gallery_item.width)
    print("Type:", gallery_item.type)
    print("Cost:", gallery_item.cost)

    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES.get('image')
        painting_type = request.POST.get('type')
        description = request.POST.get('description')
        height = request.POST.get('height')
        width = request.POST.get('width')
        cost = request.POST.get('cost')

        print(painting_type)
        
        if title:
            gallery_item.title = title
        if image_file:
            gallery_item.image = image_file
        if painting_type:
            gallery_item.type = painting_type
        if description:
            gallery_item.description = description
        if height:
            gallery_item.height = height
        if width:
            gallery_item.width = width
        if cost:
            gallery_item.cost = cost
        
        gallery_item.save()
        return redirect('dashboard_painting_for_sale_list')  # Redirect to the gallery view

    return render(request, 'dashboard/painting_for_sale_list_edit.html', {'gallery_item': gallery_item})


def painting_for_sale_list(request):
    painting_for_sale_items = PaintingForSaleModel.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        height = request.POST.get('height')
        width = request.POST.get('width')
        painting_type = request.POST.get('type')
        cost = request.POST.get('cost')
        image_file = request.FILES.get('image')

        if title and description and height and width and painting_type and cost and image_file:
            new_painting = PaintingForSaleModel(
                title=title,
                description=description,
                height=height,
                width=width,
                type=painting_type,
                cost=cost,
                image=image_file
            )
            new_painting.save()
            return redirect('dashboard_painting_for_sale_list')
    return render(request, 'dashboard/painting_for_sale_list.html',{"painting_for_sale_items":painting_for_sale_items})

def show_orders(request):
    return render(request, 'dashboard/show_orders.html')

def order(request):
    return render(request, 'dashboard/order.html')

def show_payments(request):
    return render(request, 'dashboard/show_payments.html')

def payment(request):
    return render(request, 'dashboard/payment.html')

def user_panel(request):
    users = User.objects.all()
    print(users)
    return render(request, 'dashboard/user_panel.html',{"users":users})

def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        print(request.POST)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        # Handle staff and superuser checkboxes
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        
        user.save()
        return redirect('user_edit', user_id=user.id) 
    return render(request, 'dashboard/user_edit.html',{"user":user})