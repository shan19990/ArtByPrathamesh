# Create a new middleware file if not already created, e.g., middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import BannedUser
from events.models import RecentEventsModel
from django.contrib.auth import get_user_model

class BannedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user

        if user.is_authenticated:
            try:
                banned_user = BannedUser.objects.filter(user=user , active=True).first()
                if banned_user is not None:
                    messages.error(request, "Your account is banned.")
                    return redirect(reverse('account_logout'))  # Redirect to logout URL
            except BannedUser.DoesNotExist:
                pass

        return response

User = get_user_model()

class UserCreationEventMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_user_creation(self, user):
        print("Creaing event")
        event = RecentEventsModel(event=f"User {user.username} created an account")
        event.save()

    def process_request(self, request):
        print("Process Request")
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            self.process_user_creation(user)

