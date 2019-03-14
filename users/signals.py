from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Role

__all__ = ['create_profile', 'save_profile']


@receiver(post_save, sender=User)
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
                               role=Role.objects.get(name="Trainee"))


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    When user is saved then we save his profile
    """
    instance.profile.save()
