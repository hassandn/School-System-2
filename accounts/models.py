from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models

class User(AbstractUser):
    REGISTRATION_STATUS = (
        (True, "Registered"),
        ('pending', "Pending"),
        (False, "Not Registered"),
    )
    
    national_id = models.CharField(max_length=10, unique=True)
    bio_grapht = models.TextField(null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    registration_status = models.CharField(choices=REGISTRATION_STATUS, max_length=7, default='pending')
    
    REQUIRED_FIELDS = ["password", "first_name", "last_name", "national_id"]
    
    def __str__(self):
        return self.username
    