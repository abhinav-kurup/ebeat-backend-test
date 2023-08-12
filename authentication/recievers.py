from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import *



@receiver(post_save, sender=OfficerModel)
def user_created(sender, instance, created, **kwargs):
   if created:
        my_group, _ = Group.objects.get_or_create(name=instance.post)
        user = OfficerModel.objects.get(email=instance.email)
        my_group.user_set.add(user)
