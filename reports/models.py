from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
from authentication.models import *
from django.db import models
from base.models import *
from app.models import *


class LoactionVisitModel(BaseVisit):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_location_visit", on_delete=models.PROTECT)
    location = models.ForeignKey(LocationModel, on_delete=models.PROTECT)
    
    def __float__(self):
        return self.location.name
    class Meta:
        db_table = 'location_visit'

@receiver(pre_save, sender=LoactionVisitModel)
def set_loc_visit_id(sender, instance, **kwargs):
    date = datetime.now().strftime("%Y-%B-%d")
    time = datetime.now().strftime("%H-%M-%S")
    instance.visit_id = f"location_type_{date}_{time}"




class PersonVisitModel(BaseVisit):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_person_visit", on_delete=models.PROTECT)
    person = models.ForeignKey(PersonModel, on_delete=models.PROTECT)
    def __str__(self):
        return self.person.name
    class Meta:
        db_table = 'person_visit'

@receiver(pre_save, sender=PersonVisitModel)
def set_person_visit_id(sender, instance, **kwargs):
    date = datetime.now().strftime("%Y-%B-%d")
    time = datetime.now().strftime("%H-%M-%S")
    instance.visit_id = f"Person_visit_{date}_{time}"



class GeneralVisitModel(BaseVisit):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_visit", on_delete=models.PROTECT)
    visit_to = models.CharField(max_length=50)
    def __str__(self):
        return self.person_visit_id
    class Meta:
        db_table = 'general_visit'


class SummonWarrentModel(BaseModel):
    class CategoryType(models.TextChoices):
        Summon = "Summon", "Summon"
        Warrent = "Warrent", "Warrent"
    category = models.CharField(max_length=50, choices=CategoryType.choices)
    police_station = models.ForeignKey(PoliceStationModel, related_name="police_station_order", on_delete=models.DO_NOTHING)
    assigned_to = models.ForeignKey(BeatOfficerModel, related_name="assigned_bo", on_delete=models.PROTECT)
    order_id = models.CharField(max_length=20)
    name = models.CharField( max_length=50)
    address = models.TextField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    visted_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True,blank= True)
    is_visited = models.BooleanField(default=False)
    def __str__(self):
        return self.order_id
    class Meta:
        db_table = 'summon_warrent'



class BeatOfficerLogs(BaseModel):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_logs", on_delete=models.PROTECT)
    comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.BO.name
    class Meta:
        db_table = 'bo_logs'

