from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

def custom_login_required(view_func):
    @login_required(login_url='/user/login/')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Please log in to see the cart.')
            return redirect('/user/login/?next=' + request.path)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
