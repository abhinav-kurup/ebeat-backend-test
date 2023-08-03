from django.db import models
from django.contrib.auth.models import Group
from base.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

OFFICER_POSTS = (("PI", "PI"), ("DYSP", "DYSP"), ("SP", "SP"), ("IGP", "IGP"))

class BeatOfficerModel(BaseUser):
    service_number = models.CharField(max_length=10)
    def __str__(self):
        return self.email


class SellerModel(BaseUser):
    post = models.CharField(max_length=50, choices=OFFICER_POSTS, null=True, blank=True)
    service_number = models.CharField(max_length=10)

    
    def __str__(self):
        return self.email


class Confidential(BaseModel):
    num = models.IntegerField()



@receiver(post_save, sender=SellerModel)
def user_created(sender, instance, created, **kwargs):
   if created:
                my_group = Group.objects.get(name=instance.post) 
                print(my_group)
                user = SellerModel.objects.get(email=instance.email)
                my_group.user_set.add(user)