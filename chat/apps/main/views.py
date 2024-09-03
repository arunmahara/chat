import logging

from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view

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
