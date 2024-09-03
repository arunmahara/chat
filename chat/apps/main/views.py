import logging

from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view

from chat.apps.main.forms import SignupForm, LoginForm
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


def login(request: HttpRequest) -> HttpResponse:
    """
    Handle user login.
    """
    if request.user.is_authenticated:
        log.info(f"Authenticated user {request.user.username} tried to access login page")
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username: str = form.cleaned_data['username']
            password: str = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                request.session['access_token'] = get_access_token(user)
                log.info(f"User {username} logged in successfully")

                return redirect('home')
            else:
                log.warning(f"Authentication failed for user {username}")
        else:
            log.warning("Login form is invalid")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@jwt_required
def home(request: HttpRequest) -> HttpResponse:
    """
    Home view to create and list chat rooms.
    """
    log.info(f"User {request.user.username} accessed home page")
    if request.method == 'POST':
        return create_room(request)

    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


@jwt_required
def create_room(request: HttpRequest) -> HttpResponse:
    """
    Helper function to create a new chat room.
    """
    new_room = request.POST['room']
    if Room.objects.filter(name=new_room).exists():
        messages.warning(request, 'Room Already Exists')
        log.warning(f"User {request.user.username} tried to create an existing room: {new_room}")
    else:
        room = Room(name=new_room, created_by=request.user)
        room.save()

        messages.success(request, 'Room Created')
        log.info(f"User {request.user.username} created a new room: {new_room}")

    return redirect('home')
