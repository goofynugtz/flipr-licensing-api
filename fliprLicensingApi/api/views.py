from .utils import validate_signature, generate_license
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone
from accounts.models import Employee
from prometheus_client import Counter, generate_latest
from decouple import config
from .models import License, Policy
from .serializers import LicenseSerializer
import jwt
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from .utils import timestamps

API_REFRESH_RATE = getattr(settings, 'API_REFRESH_RATE', 10)
LICENSES_TTL = 60*60*24

counter = {
  'success': Counter('total_successful_validations', 'Total no. of successful validation requests'),
  'failed': Counter('total_failed_validations', 'Total no. of failed validation requests'),
  'issued': Counter('total_licenses_issued', 'Total no. of license keys issued'),
  'suspended': Counter('total_licenses_suspended', 'Total no. of license keys suspended'),
  'revoked': Counter('total_licenses_revoked', 'Total no. of license keys revoked')
}

# Header { "Authorization": "Bearer JWT" }
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentlyOnlineUsers(request):
  users = Employee.objects.all()
  counter = sum(1 for user in users if cache.get(user.email))
  return Response(counter, status=status.HTTP_200_OK)


# Header { "Authorization": "Bearer JWT" }
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def licenses(request):
  license_records = License.objects.all()
  serializer = LicenseSerializer(license_records, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


# Body { "email", "key" }
@api_view(['GET'])
@permission_classes([AllowAny])
def validate(request):
  email = request.data["email"].lower()
  key = request.data['key']
  if cache.get([email, key]):
    # Asterisk denotes Server timestamp, 
    # See: https://redis-py.readthedocs.io/en/stable/examples/timeseries_examples.html
    timestamps.add(user.email, "*", 1) 
    return Response(cache.get([email, key]), status=status.HTTP_200_OK)
  try:
    user = Employee.objects.get(email=email)
    if user.is_verified == True:
      cache.set(user.email, True, API_REFRESH_RATE)
      try:
        license_record = License.objects.get(user=user)
        if (validate_signature(email=email, license_key=key, public_key=license_record.public_key)):
          if (license_record.validUpto < timezone.now()):
            record_status = { "status": License.EXP, }
            license_serializer = LicenseSerializer(instance=license_record, data=record_status, partial=True)
            if (license_serializer.is_valid()):
              license_serializer.save()
            counter['failed'].inc()
            cache.set([email, key], license_record.status, LICENSES_TTL)
            return Response(license_record.status, status=status.HTTP_406_NOT_ACCEPTABLE)
          else: 
            counter['success'].inc()
            timestamps.add(user.email, "*", 1)
            cache.set([email, key], license_record.status, LICENSES_TTL)
            return Response(license_record.status, status=status.HTTP_200_OK)
        else:
          counter['failed'].inc()
          return Response("INVALID", status=status.HTTP_406_NOT_ACCEPTABLE)
      except ObjectDoesNotExist:
        counter['failed'].inc()
        return Response("NOT_FOUND", status=status.HTTP_404_NOT_FOUND)
    return Response("USER_SCOPE_MISMATCH", status=status.HTTP_403_FORBIDDEN)
  except ObjectDoesNotExist:
    counter['failed'].inc()
    return Response("USER_SCOPE_MISMATCH", status=status.HTTP_403_FORBIDDEN)


# Header { "Authorization": "Bearer JWT" } 
# Body   { "name", "policy"}
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def issue(request):
  access_token = request.headers['Authorization'].split(' ')[-1]
  name = request.data["name"]
  policy_name = request.data["policy"]
  try: 
    policy = Policy.objects.get(name=policy_name)
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    try:
      user = Employee.objects.get(email=email)
      timestamps.add(user.email, "*", 1)
      if user.is_verified == True:
        previous_license = License.objects.filter(user=user)
        if (len(previous_license) > 0):
            previous_license.delete()
        validUpto = timezone.now() + policy.validity
        # Passing rest process to Celery: 
        # See: https://docs.celeryq.dev/en/stable/userguide/calling.html
        generate_license.delay(name, email, policy.id, validUpto)
        counter['issued'].inc()
        return Response({
          "detail": "License key has been mailed"
        }, status=status.HTTP_201_CREATED)
      return Response({
        "detail": "User not verified"
      }, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
      return Response({
        "detail": "Employee / Email does not exist"
      }, status=status.HTTP_400_BAD_REQUEST)
  except ObjectDoesNotExist:
    return Response({
      "detail": "Invalid policy"
    }, status=status.HTTP_404_NOT_FOUND)


# Header { "Authorization": "Bearer JWT" } 
# Body   { "email" }
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def suspend(request):
  email = request.data['email']
  try:
    user = Employee.objects.get(email=email)
    license_record = License.objects.get(user=user)
    record_status = { "status": License.SUS, }
    license_serializer = LicenseSerializer(instance=license_record, data=record_status, partial=True)
    if license_serializer.is_valid():
      license_serializer.save()
      counter['suspended'].inc()
      return Response({
        "detail": "License suspended"
      }, status=status.HTTP_202_ACCEPTED)
    return Response({
      "detail": "Something went wrong"
    }, status=status.HTTP_400_BAD_REQUEST)
  except ObjectDoesNotExist:
    return Response({
      "detail": "Employee / License does not exist"
    }, status=status.HTTP_401_UNAUTHORIZED)


# Header { "Authorization": "Bearer JWT" } 
# Body   { "email" }
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def resume(request):
  email = request.data['email']
  try:
    user = Employee.objects.get(email=email)
    license_record = License.objects.get(user=user)
    record_status = { "status": License.VAL, }
    license_serializer = LicenseSerializer(instance=license_record, data=record_status, partial=True)
    if license_serializer.is_valid():
      license_serializer.save()
      return Response({
        "detail": "License status Continued"
      }, status=status.HTTP_202_ACCEPTED)
    return Response({
      "detail": "Something went wrong"
    }, status=status.HTTP_400_BAD_REQUEST)
  except ObjectDoesNotExist:
    return Response({
      "detail": "Employee / License does not exist"
    }, status=status.HTTP_401_UNAUTHORIZED)


# Header { "Authorization": "Bearer JWT" } 
# Body   { "email" }
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke(request):
  email = request.data['email']
  try:
    user = Employee.objects.get(email=email)
    license_record = License.objects.get(user=user)
    license_record.delete()
    counter['revoked'].inc()
    return Response({
      "detail": "License deleted"
    }, status=status.HTTP_200_OK)
  except:
    return Response({
      "detail": "Employee / License does not exists"
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def compute_metrics(request):
  res = []
  for _, value in counter.items():
    res.append(generate_latest(value))
  return HttpResponse(res, content_type="text/plain")
