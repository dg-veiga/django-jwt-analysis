from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    if request.method == 'GET':
        return JsonResponse({'msg': 'success'})
