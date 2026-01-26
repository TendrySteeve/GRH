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
        ordering = ['-created_at']
        verbose_name = "Planning"
        verbose_name_plural = "Plannings"

  class Meta:
      ordering = ['date']


class Leave(models.Model):

    LEAVE_TYPE_CHOICES = [
        ('AN', 'Congé annuel'),
        ('CM', 'Congé de maternité'),
        ('CP', 'Congé de paternité'),
        ('ML', 'Maladie'),
        ('SP', 'Sans solde'),
        ('AU', 'Autorisation spéciale'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Rejeté'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leaves'
    )

    leave_type = models.CharField(
        max_length=2,
        choices=LEAVE_TYPE_CHOICES
    )

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Congé"
        verbose_name_plural = "Congés"

    def __str__(self):
        return f"{self.user} - {self.get_leave_type_display()} ({self.start_date} → {self.end_date})"