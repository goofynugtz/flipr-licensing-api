from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Organization
from .utils import send_password_reset_mail
import uuid

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
  Employee.objects.create(name=name, email=email, organization=organization, phone=phone, emp_address=address)
  user = Employee.objects.get(email=email)
  user.set_password(password)
  user.save()
  return Response("User signed up", status=status.HTTP_201_CREATED)

# Body { "email" }
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_request(request):
  email = request.data['email']
  try:
    user = Employee.objects.get(email=email)
    token = uuid.uuid4()
    user.password_reset_token = token
    print(user)
    user.save()
    send_password_reset_mail(email, token)
    return Response("Reset link has been sent on email.", status=status.HTTP_200_OK)
  except ObjectDoesNotExist:
    return Response("No user found with this email.", status=status.HTTP_204_NO_CONTENT)

# Body { "password" }
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token):
  try:
    user = Employee.objects.get(password_reset_token=token)
    password = request.data['password']
    user.set_password(password)
    user.password_reset_token = None
    print(user)
    user.save()
    return Response("Password reset successfull.", status=status.HTTP_202_ACCEPTED)
  except ObjectDoesNotExist:
    return Response("Password reset token has expired.", status=status.HTTP_403_FORBIDDEN)
