from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class CustomObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def webhook(request):
    print(request.headers)
    print(request.data)
    return Response('success', status=status.HTTP_200_OK)
