from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SUBSCRIBER', 'Subscriber/User'),
        ('CREATOR', 'Creator/Content Owner'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SUBSCRIBER')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
