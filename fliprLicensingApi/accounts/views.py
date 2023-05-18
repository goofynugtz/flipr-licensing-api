from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.transaction import atomic, non_atomic_requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def webhook(request):
    print(request)
    print("\n")
    print(request.headers)
    print("\n")
    print(request.data)
    print("\n")
    # OutstandingToken.objects.create
    return Response('success', status=status.HTTP_200_OK)
