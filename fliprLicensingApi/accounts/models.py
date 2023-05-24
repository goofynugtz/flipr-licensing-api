from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import EmployeeManager
import uuid

class Organization(models.Model):
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  title = models.CharField(max_length=255, unique=True)
  url = models.URLField(null=True, blank=True)
  org_address = models.CharField(max_length=1024, null=True, blank=True)

  def __str__(self):
    return self.title

class Employee(AbstractUser, PermissionsMixin):
  username = None
  name = models.CharField("Name", max_length=255)
  email = models.EmailField("Email Address", unique=True)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
  phone = models.CharField("Phone", max_length=14, unique=True, null=True, blank=True)
  emp_address = models.CharField(max_length=1024, blank=True, null=True)
  password_reset_token = models.UUIDField(default=uuid.uuid4, null=True, editable=False)
  confirmation_token = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
  is_verified = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']
  objects = EmployeeManager()
  
  def __str__(self) -> str:
    return self.name
