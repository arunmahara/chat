from rest_framework import status
from rest_framework.decorators import api_view

from chat.core.response import generic_response


@api_view(['GET'])
def health(request):
    result = {
        'status': "healthy"
    }

    return generic_response(
        success=True,
        message="Health check",
        data=result,
        status=status.HTTP_200_OK
    )
