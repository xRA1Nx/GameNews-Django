from .models import User
from django.dispatch import receiver


from django.db.models.signals import post_save
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def add_group_on_create(instance, **kwargs):
    common_group = Group.objects.get(name='common')
    common_group.user_set.add(instance)
