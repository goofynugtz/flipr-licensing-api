from django.db import models
import uuid
from accounts.models import Employee

class License(models.Model):
    VALIDATION_CODES = [
        ("VALID", "Valid"),
        ("SUSPENDED", "Suspended"), 
        ("EXPIRED", "Expired"), 
        ("USER_SCOPE_MISMATCH", "Incorrect Email")
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=1024, unique=True, editable=False)
    status = models.CharField(max_length=255, choices=VALIDATION_CODES, default="VALID")
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name