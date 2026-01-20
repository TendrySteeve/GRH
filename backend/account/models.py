from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  ROLE_CHOICES = (
    ('ADMIN', 'Administrateur'),
    ('RESP', 'Responsable'),
    ('EMPLOYEE', 'Employé'),
  )

  role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
  phone = models.CharField(max_length=13, blank=True, null=True)
  
