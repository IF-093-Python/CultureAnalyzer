from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from CultureAnalyzer.constants import TRAINEE_ID, ADMIN_ID
from users.models import LoggedInUser

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
        if instance.is_superuser:
            Group.objects.get(pk=ADMIN_ID).user_set.add(instance)
        else:
            Group.objects.get(pk=TRAINEE_ID).user_set.add(instance)


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
