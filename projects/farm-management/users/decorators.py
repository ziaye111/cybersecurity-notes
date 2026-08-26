from functools import wraps

from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied

        return wrapped_view

    return decorator