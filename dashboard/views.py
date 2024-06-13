from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from marketplace.models import *
from user.models import *
from django.contrib import messages
from events.models import *

def dashboard(request):
    recent_events = RecentEventsModel.objects.order_by('-id')[:50]
    return render(request, 'dashboard/dashboard.html',{"recent_events":recent_events})

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
    user_details = []

    for user in users:
        banned_user = BannedUser.objects.filter(user=user , active=True).first()
        if banned_user and banned_user.active:
            banned_till = banned_user.banned_till
            banned_status = True
        else:
            banned_till = ""
            banned_status = False
        
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'banned': banned_status,
            'banned_till': banned_till
        }
        user_details.append(user_info)

    return render(request, 'dashboard/user_panel.html', {"users": user_details})




def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    banned_user = BannedUser.objects.filter(user=user, active=True).first()

    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.is_staff = 'is_staff' in request.POST
        user.is_superuser = 'is_superuser' in request.POST
        user.save()

        # Handle banning user
        is_banned = request.POST.get('is_banned', False)
        ban_reason = request.POST.get('reason', '')
        banned_till = request.POST.get('till')

        if is_banned:
            if banned_till:
                banned_till_date = timezone.datetime.strptime(banned_till, '%Y-%m-%d').date()
            else:
                banned_till_date = None

            if banned_user:
                # Update existing banned_user instance
                banned_user.reason = ban_reason
                banned_user.banned_till = banned_till_date
                banned_user.active = True
                banned_user.save()
            else:
                BannedUser.objects.create(user=user, reason=ban_reason, banned_till=banned_till_date, active=True)
        else:
            if banned_user:
                banned_user.active = False
                banned_user.save()

        messages.success(request, 'User information updated successfully.')
        return redirect('user_edit', user_id=user_id)

    user_info = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'banned': banned_user.active if banned_user else False,
        'banned_till': banned_user.banned_till if banned_user else None,
        'ban_reason': banned_user.reason if banned_user else None
    }

    return render(request, 'dashboard/user_edit.html', {'user': user_info})



