from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Organization
from .utils import send_password_reset_mail, send_verification_mail
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

class CustomObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['email'] = user.email
    return token

class CustomObtainPairView(TokenObtainPairView):
  serializer_class = CustomObtainPairSerializer


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
    'test': str("hello")
  }

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login(request):
#   email = request.data["email"]
#   user = Employee.objects.get(email=email)
#   try:
#     if user.is_verified == True:

# Body { "name", "email", "password", "organization", "phone", "address" }
@api_view(['POST'])
@permission_classes([AllowAny])
def first_signup(request):
  email = request.data["email"]
  user = Employee.objects.filter(email=email)
  if (len(user) > 0):
    return Response("Already exists", status=status.HTTP_208_ALREADY_REPORTED)
  
  name = request.data["name"]
  password = request.data["password"]
  organization = request.data["organization"]
  organization = Organization.objects.get(title=organization)
  phone = request.data["phone"]
  address = request.data["address"]
  
  confirmation_token = uuid.uuid4()
  Employee.objects.create(name=name, password=password, email=email, organization=organization, phone=phone, emp_address=address, confirmation_token=confirmation_token)
  send_verification_mail(email, confirmation_token)

  user = Employee.objects.get(email=email)
  user.set_password(password)
  user.save()

  return Response("Verification email has been sent.", status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_signup(request, token):
  try:
    user = Employee.objects.get(confirmation_token=token)
    user.is_verified = True
    user.confirmation_token = None
    user.save()
    
    return Response("User verification complete.", status=status.HTTP_200_OK)
  except ObjectDoesNotExist:
    return Response("Email not found.", status=status.HTTP_404_NOT_FOUND)


# Body { "email" }
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_request(request):
  email = request.data['email']
  try:
    user = Employee.objects.get(email=email)
    if user.is_verified == True:
      token = uuid.uuid4()
      user.password_reset_token = token
      user.save()
      send_password_reset_mail(email, token)
      return Response("Reset link has been sent on email.", status=status.HTTP_200_OK)
    return Response("User not verified.", status=status.HTTP_304_NOT_MODIFIED)
  except ObjectDoesNotExist:
    return Response("No user found with this email.", status=status.HTTP_204_NO_CONTENT)

# Body { "password" }
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token):
  try:
    user = Employee.objects.get(password_reset_token=token)
    if user.is_verified == True:
      password = request.data['password']
      user.set_password(password)
      user.password_reset_token = None
      user.save()
      return Response("Password reset successfull.", status=status.HTTP_202_ACCEPTED)
    return Response("User not verified.", status=status.HTTP_304_NOT_MODIFIED)
  except ObjectDoesNotExist:
    return Response("Password reset token has expired.", status=status.HTTP_403_FORBIDDEN)
