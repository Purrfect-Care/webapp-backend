from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if "employee_id" not in request.session:
            return redirect(reverse('login'))
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view