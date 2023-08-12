from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db import models
from base.models import *
from .managers import *



class OfficerModel(BaseUser):
    class PolicePost(models.TextChoices):
        SP = "SP", "Superintendent of Police"
        DYSP = "DYSP", "Deputy Superintendent of Police"
        PI = "PI", "Police Inspector"
        IGP = "IGP", "Inspector-General of Police"
    post = models.CharField(max_length=50, choices=PolicePost.choices)
    service_number = models.CharField(max_length=10)
    admin_objects = models.Manager()
    igp_objects = IGPManager()
    sp_objects = SPManager()
    dysp_objects = DYSPManager()
    pi_objects = PIManager()
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'officer'


class StateModel(BasePolygon):
    igp = models.OneToOneField(OfficerModel, on_delete=models.CASCADE, null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'state'

class DistrictModel(BasePolygon):
    sp = models.OneToOneField(OfficerModel, on_delete=models.CASCADE, null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    state = models.ForeignKey(StateModel, related_name="districts", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'district'

class SubDivisionModel(BasePolygon):
    dysp = models.OneToOneField(OfficerModel, on_delete=models.CASCADE, null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    district = models.ForeignKey(DistrictModel, related_name="sub_divisions", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'sub_division'

class PoliceStationModel(BasePolygon):
    pi = models.OneToOneField(OfficerModel, on_delete=models.CASCADE, null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    sub_division = models.ForeignKey(SubDivisionModel, related_name="police_stations", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'police_station'


class BeatAreaModel(BasePolygon):
    beat_no = models.IntegerField(unique=True)
    police_station = models.ForeignKey(PoliceStationModel, related_name="beats", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'beat_area'


class BeatOfficerModel(BaseUser):
    police_station = models.ForeignKey(PoliceStationModel, related_name="Police_Station_BOs", on_delete=models.CASCADE)
    beat_area = models.ForeignKey(BeatAreaModel, related_name="bo_of_ba", on_delete=models.DO_NOTHING, null=True, blank=True)
    service_number = models.CharField(max_length=10)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'beat_officer'



@receiver(post_save, sender=OfficerModel)
def user_created(sender, instance, created, **kwargs):
   if created:
        my_group, _ = Group.objects.get_or_create(name=instance.post) 
        user = OfficerModel.objects.get(email=instance.email)
        my_group.user_set.add(user)




