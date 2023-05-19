from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.transaction import atomic, non_atomic_requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from accounts.models import Employee
from prometheus_client import Counter, generate_latest
from decouple import config
from .utils import validate_signature, generate_license, new_rsa, mail_license_keys
from .models import License
from .serializers import LicenseSerializer
import jwt

counter = {
    'success': Counter('total_successful_validations', 'Total no. of successful validation requests'),
    'failed': Counter('total_failed_validations', 'Total no. of failed validation requests'),
    'issued': Counter('total_licenses_issued', 'Total no. of license keys issued'),
    'suspended': Counter('total_licenses_suspended', 'Total no. of license keys suspended'),
    'revoked': Counter('total_licenses_revoked', 'Total no. of license keys revoked')
}

@api_view(['GET'])
@permission_classes([AllowAny])
@non_atomic_requests
def validate(request):
    email = request.data["email"].lower()
    try:
        user = Employee.objects.get(email=email)
        try:
            # WARN: Still not checking valid upto status.
            license_record = License.objects.get(user=user)
            if (validate_signature(email=request.data['email'], license_key=request.data['key'], public_key=license_record.public_key)):
                counter['success'].inc()
                return Response(license_record.status, status=status.HTTP_200_OK)
            else:
                counter['failed'].inc()
                return Response("INVALID", status=status.HTTP_406_NOT_ACCEPTABLE)
        except ObjectDoesNotExist:
            counter['failed'].inc()
            return Response("INVALID", status=status.HTTP_406_NOT_ACCEPTABLE)
    except ObjectDoesNotExist:
        counter['failed'].inc()
        return Response("USER_SCOPE_MISMATCH", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@atomic
def issue(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    name = request.data["name"]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    try:
        user = Employee.objects.get(email=email)
        previous_license = License.objects.filter(user=user)
        if (len(previous_license) > 0):
            previous_license.delete()
        public_key, private_key = new_rsa()
        key = generate_license(email, private_key)
        License.objects.create(
            name = name,
            key = key,
            public_key = public_key,
            private_key = private_key,
            user = user
        )
        mail_license_keys(key, email)
        counter['issued'].inc()
        return Response("Success", status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        return Response("Employee/Email does not exist.", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@non_atomic_requests
def suspend(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    try:
        user = Employee.objects.get(email=email)
        license_record = License.objects.get(user=user)
        modified_data = {
            "name": license_record.name,
            "status": "SUSPENDED",
        }
        license_serializer = LicenseSerializer(instance=license_record, data=modified_data)
        if license_serializer.is_valid():
            license_serializer.save()
            counter['suspended'].inc()
            return Response("License Suspended", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Something went wrong", status=status.HTTP_304_NOT_MODIFIED)
    except ObjectDoesNotExist:
        return Response("Employee/License does not exists.", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@non_atomic_requests
def resume(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    try:
        user = Employee.objects.get(email=email)
        license_record = License.objects.get(user=user)
        modified_data = {
            "name": license_record.name,
            "status": "VALID",
        }
        license_serializer = LicenseSerializer(instance=license_record, data=modified_data)
        if license_serializer.is_valid():
            license_serializer.save()
            return Response("License status continued", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Something went wrong", status=status.HTTP_304_NOT_MODIFIED)
    except ObjectDoesNotExist:
        return Response("Employee/License does not exists.", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@non_atomic_requests
def revoke(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    try:
        user = Employee.objects.get(email=email)
        license_record = License.objects.get(user=user)
        license_record.delete()
        counter['revoked'].inc()
        return Response("Deleted", status=status.HTTP_200_OK)
    except:
        return Response("Employee/License does not exists.", status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
# WARN: AllowAny
@permission_classes([AllowAny])
@non_atomic_requests
def compute_metrics(request):
    res = []
    for _, value in counter.items():
        res.append(generate_latest(value))
    return HttpResponse(res, content_type="text/plain")
