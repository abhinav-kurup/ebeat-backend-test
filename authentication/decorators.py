from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            if request.user.is_authenticated and request.user.is_active == True:
                group = None
                if request.user.groups.exists():
                    group=request.user.groups.all()[0].name
                
                if group in allowed_roles:
                    return view_func(request,*args,**kwargs)
                else:
                    return HttpResponse('You are not authorised',status=404)
            
        return wrapper_func
    return decorator





    
