from functools import wraps
from typing import Callable, Optional, Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def get_access_token(user: AbstractBaseUser) -> str:
    """
    Generate an access token for the given user.
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def validate_jwt(token: str) -> Optional[AbstractBaseUser]:
    """
    Validate the given JWT token and return the associated user if valid.
    """
    try:
        payload = AccessToken(token).payload
        user_id = payload.get(settings.SIMPLE_JWT["USER_ID_CLAIM"])
        user = get_user_model().objects.get(id=user_id, is_active=True)
        return user
    except Exception:
        return None


def jwt_required(f: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """
    Decorator to ensure the request has a valid JWT token.
    """
    @wraps(f)
    def decorated_function(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        token = request.session.get('access_token', None)

        if not token:
            return redirect('/')

        user = validate_jwt(token)
        if not user:
            return redirect('/')

        request.user = user
        return f(request, *args, **kwargs)

    return decorated_function
