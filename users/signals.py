from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Role, CustomUser

__all__ = ['create_profile', 'save_profile']


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """
    When sender is saved we send signal post_save
    this signal is receive by @receiver
    this receiver is create_profile,
    in create_profile method we check if instance was created
    then we create profile

    """
    if created:
        Profile.objects.create(user=instance,
                               role=get_role(instance))


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    """
    When user is saved then we save his profile
    """
    instance.profile.save()


def get_role(instance):
    if instance.is_superuser:
        return Role.objects.get(name='Admin')
    return Role.objects.get(name='Trainee')
