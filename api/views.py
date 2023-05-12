from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .utils import valid, generate_license, new_rsa
import jwt
from decouple import config
from .models import License
from django.contrib.auth.models import User
from .serializers import LicenseSerializer
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
@permission_classes([AllowAny])
def validate(request):
    data = request.data
    # WARN: More checks required
    if (valid(data['email'], data['key'])):
        return Response("VAL", status=status.HTTP_200_OK)
    else:
        return Response("INV", status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def issue(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    name = request.data["name"]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    print(email)
    try:
        user = User.objects.get(email=email)
        print(user)
        public, private = new_rsa()
        print(private) 
        print(public)
        key = generate_license(email, private)
        print(key)
        License.objects.create(
            name = name,
            key = key,
            public_key = public,
            private_key = private,
            user = user
        )
        return Response(key, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        return Response("User/Email does not exist.", status=status.HTTP_400_BAD_REQUEST)
