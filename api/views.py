from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .utils import validate_signature, generate_license, new_rsa
import jwt
from decouple import config
from .models import License
from .serializers import LicenseSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import prometheus_client
from prometheus_client import Counter

counter = {
    'success': Counter('total_successful_validations', 'Total no. of successful validation requests'),
    'failed': Counter('total_failed_validations', 'Total no. of failed validation requests'),
    'issued': Counter('total_licenses_issued', 'Total no. of license keys issued'),
    'suspended': Counter('total_licenses_suspended', 'Total no. of license keys suspended'),
    'revoked': Counter('total_licenses_revoked', 'Total no. of license keys revoked')
}

@api_view(['GET'])
@permission_classes([AllowAny])
def validate(request):
    try:
        user = User.objects.get(email=request.data["email"])
        try:
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
def issue(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    name = request.data["name"]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    try:
        user = User.objects.get(email=email)
        public_key, private_key = new_rsa()
        key = generate_license(email, private_key)
        License.objects.create(
            name = name,
            key = key,
            public_key = public_key,
            private_key = private_key,
            user = user
        )
        counter['issued'].inc()
        return Response(key, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        return Response("User/Email does not exist.", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suspend(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    print(email)
    try:
        user = User.objects.get(email=email)
        print(user.username)
        license_record = License.objects.get(user=user)
        print(license_record)
        # license_serializer = LicenseSerializer(instance=license_record, data=?)
        # print(license_serializer.data)
        # print(license_serializer.is_valid())
        # license_serializer.save()
        counter['suspended'].inc()
        return Response("License Suspended", status=status.HTTP_202_ACCEPTED)
    except:
        return Response("User/License does not exists.", status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke(request):
    access_token = request.headers['Authorization'].split(' ')[-1]
    data = jwt.decode(access_token, algorithms=['HS256'], key=config('SECRET_KEY'))
    email = data['email']
    print(email)
    try:
        user = User.objects.get(email=email)
        license_record = License.objects.get(user=user)
        license_record.delete()
        counter['revoked'].inc()
        return Response("Deleted", status=status.HTTP_200_OK)
    except:
        return Response("User/License does not exists.", status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
# WARN: AllowAny
@permission_classes([AllowAny])
def compute_metrics(request):
    res = []
    for _, value in counter.items():
        res.append(prometheus_client.generate_latest(value))
    return HttpResponse(res, content_type="text/plain")