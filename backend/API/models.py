from django.db import models

from account.models import User


class Schedule(models.Model):
    STATUS_CHOICE = [
        ("TT", "Télétravail"),
        ("R", "Réunion"),
        ("CM", "Congés de matérnité"),
        ("MI", "Mission"),
        ("P", "Permission"),
        ("M", "Maladie"),
        ("F", "Formation"),
        ("REC", "Récupération"),
        ("SS", "Sur site"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="schedule_events"
    )

    date = models.DateField()

    status = models.CharField(max_length=3, choices=STATUS_CHOICE)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Planning"
        verbose_name_plural = "Plannings"

    class Meta:
        ordering = ["date"]


class Leave(models.Model):

    LEAVE_TYPE_CHOICES = [
        ("AN", "Congé annuel"),
        ("CM", "Congé de maternité"),
        ("CP", "Congé de paternité"),
        ("ML", "Maladie"),
        ("SP", "Sans solde"),
        ("AU", "Autorisation spéciale"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "En attente"),
        ("APPROVED", "Approuvé"),
        ("REJECTED", "Rejeté"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="leaves", verbose_name="Employé"
    )

    leave_type = models.CharField(
        max_length=2, choices=LEAVE_TYPE_CHOICES, verbose_name="Type de congé"
    )

    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")

    reason = models.TextField(blank=True, verbose_name="Motif")

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING", verbose_name="Statut"
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_leaves",
        verbose_name="Validé par",
    )

    approved_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Date de validation"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Congé"
        verbose_name_plural = "Congés"

    def __str__(self):
        return (
            f"{self.user} | "
            f"{self.get_leave_type_display()} | "
            f"{self.start_date} → {self.end_date}"
        )
