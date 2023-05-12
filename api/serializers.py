from rest_framework.serializers import ModelSerializer
from .models import License

class LicenseSerializer(ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'