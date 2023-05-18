from django.db import models
import uuid, datetime
from django.utils import timezone
from django.contrib.auth.models import User

class License(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=1024, unique=True, editable=False)
    public_key = models.CharField(max_length=2048, null=True, editable=False)
    private_key = models.CharField(max_length=2048, null=True, editable=False)
    status = models.CharField(max_length=255, default="VALID")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    validUpto = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=365))
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name