from functools import wraps
from django.http import HttpResponseRedirect

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user' not in request.session:
            return HttpResponseRedirect('/login/?next=%s' % request.path)
        return view_func(request, *args, **kwargs)
    return _wrapped_view