from django.db import models
from django.contrib.auth.models import User
import uuid

class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.title

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=14)

    def __str__(self):
        return f"{self.user.username}"