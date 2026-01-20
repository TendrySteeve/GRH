from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_admin_role_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser and instance.role != "ADMIN":
        instance.role = "ADMIN"
        instance.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def deactivate_new_users(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        instance.is_active = False
        instance.save()
