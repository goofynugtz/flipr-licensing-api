from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .manager import EmployeeManager
from .models import Employee, Organization
from rest_framework import exceptions, serializers
from django.http import HttpResponseRedirect

class CustomObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['email'] = user.email
    return token

class CustomObtainPairView(TokenObtainPairView):
  serializer_class = CustomObtainPairSerializer

# Body { "name", "email", "password", "organization", "phone", "address" }
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
  name = request.data["name"]
  email = request.data["email"]
  password = request.data["password"]
  organization = request.data["organization"]
  organization = Organization.objects.get(title=organization) # Not a primary key
  phone = request.data["phone"]
  address = request.data["address"]
  user = Employee.objects.filter(email=email)
  if (len(user) > 0):
    return Response("Already exists", status=status.HTTP_208_ALREADY_REPORTED)
  Employee.objects.create(name=name, email=email, organization=organization, phone=phone, address=address)
  user = Employee.objects.get(email=email)
  user.set_password(password)
  user.save()
  return Response("User signed up", status=status.HTTP_201_CREATED)