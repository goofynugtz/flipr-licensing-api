from rest_framework.serializers import ModelSerializer, DurationField
from .models import License, Policy

class LicenseSerializer(ModelSerializer):
  class Meta:
    model = License
    fields = ('name', 'key', 'user', 'status', 'validUpto')

class PolicySerializer(ModelSerializer):
  class Meta:
    model = Policy
    fields = ('name', 'description', 'validity')
  validity = DurationField(allow_null=True)
