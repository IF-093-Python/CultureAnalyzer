from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def protected_view(request):
    return Response({'username': f'{request.user.username}'})
