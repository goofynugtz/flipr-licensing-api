from django.db import models
import uuid, datetime
from accounts.models import Employee

class Policy(models.Model):
  MINUTE = datetime.timedelta(seconds=120) # CASE: This is for testing purpose only. Will be removed.
  DAY = datetime.timedelta(days=1)
  WEEK = datetime.timedelta(weeks=1)
  MONTH = datetime.timedelta(weeks=4)
  VALIDITY_CHOICES = (
    (MINUTE, 'Minute'),
    (DAY, 'Day'),
    (WEEK, 'Week'),
    (MONTH, 'Month'),
  )
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  name = models.CharField(max_length=255, unique=True)
  description = models.CharField(max_length=1024, blank=True, null=True)
  validity = models.DurationField(blank=True, null=True, choices=VALIDITY_CHOICES)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = "Policies"

class License(models.Model):
  VAL = "VALID"
  SUS = "SUSPENDED"
  EXP = "EXPIRED"
  STATUS_CHOICES = (
    (VAL, 'Valid'),
    (SUS, 'Suspended'),
    (EXP, 'Expired'),
  )
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  name = models.CharField(max_length=255)
  key = models.CharField(max_length=1024, unique=True, editable=False)
  public_key = models.CharField(max_length=2048, null=True, editable=False)
  private_key = models.CharField(max_length=2048, null=True, editable=False)
  status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=VAL)
  user = models.ForeignKey(Employee, on_delete=models.CASCADE)
  policy = models.ForeignKey(Policy, on_delete=models.PROTECT, null=True, blank=True)
  validUpto = models.DateTimeField(null=True)
  updatedAt = models.DateTimeField(auto_now=True)
  createdAt = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
