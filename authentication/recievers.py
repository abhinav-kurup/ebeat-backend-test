from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import *
from firebase_init import firebase_admin



@receiver(post_save, sender=OfficerModel)
def user_created(sender, instance, created, **kwargs):
   if created:
      my_group, _ = Group.objects.get_or_create(name=instance.post)
      user = OfficerModel.objects.get(email=instance.email)
      my_group.user_set.add(user)


@receiver(post_save, sender=BeatOfficerModel)
def add_to_firebase(sender, instance, created, **kwargs):
   if created:
      db = firebase_admin.firestore.client()
      collection_ref = db.collection(str(instance.tid))
      doc_ref = collection_ref.add({
         'lat': 0.0,
         'lon': 0.0,
      })