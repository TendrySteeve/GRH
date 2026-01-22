from django.db import models

from account.models import User

class Schedule(models.Model):
  STATUS_CHOICE = [
    ('TT', 'Télétravail'),
    ('R', 'Réunion'),
    ('CM', 'Congés de matérnité'),
    ('MI', 'Mission'),
    ('P', 'Permission'),
    ('M', 'Maladie'),
    ('F', 'Formation'),
    ('REC', 'Récupération'),
    ('SS', 'Sur site')
  ]
  
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_events')

  date = models.DateField()

  status = models.CharField(max_length=3, choices=STATUS_CHOICE)
  description = models.TextField(blank=True)

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
      ordering = ['date']