import logging

from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view

from chat.apps.main.forms import SignupForm
from chat.apps.main.models import Room, Chat
from chat.services.authentication import get_access_token, jwt_required
from chat.core.response import generic_response

log = logging.getLogger(__name__)


@api_view(['GET'])
def health(request: HttpRequest) -> HttpResponse:
    """
    Health check endpoint.
    """
    log.info("Health check endpoint called")

    result = {
        'status': "healthy"
    }
    return generic_response(
        success=True,
        message="Health check",
        data=result,
        status=status.HTTP_200_OK
    )


def signup(request: HttpRequest) -> HttpResponse:
    """
    Handle user signup.
    """
    if request.user.is_authenticated:
        log.info(f"Authenticated user {request.user.username} tried to access signup page")
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            request.session['access_token'] = get_access_token(user)
            log.info(f"New user {user.username} signed up successfully")

            return redirect('home')
        else:
            log.warning("Signup form is invalid")
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
