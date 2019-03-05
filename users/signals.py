from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.dispatch import receiver

__all__ = ['add_group']


@receiver(post_save, sender=get_user_model())
def add_group(sender, instance, created, **kwargs):
    """
    When sender is saved we send signal post_save
    this signal is receive by @receiver
    this receiver is add_group,
    in add_group method we check if instance was created
    then we add this instance into group
    """
    if created:
        Group.objects.get(name='Trainee').user_set.add(instance)


