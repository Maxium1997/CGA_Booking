from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def superuser_check():
    def decorator(view):
        @login_required
        def check(request, *args, **kwargs):
            if not request.user.is_superuser:
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return check
    return decorator
