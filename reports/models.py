from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import *
from django.db import models
from base.models import *
from app.models import *


class LoactionVisitModel(BaseVisit):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_location_visit", on_delete=models.PROTECT)
    location = models.ForeignKey(LocationModel, on_delete=models.PROTECT)
    situation = models.FloatField(default=5.0, validators=[MaxValueValidator(10.0), MinValueValidator(0.0)])
    def __str__(self):
        return self.locaiton_visit_id
    class Meta:
        db_table = 'location_visit'


class PersonVisitModel(BaseVisit):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_person_visit", on_delete=models.PROTECT)
    person = models.ForeignKey(PersonModel, on_delete=models.PROTECT)
    def __str__(self):
        return self.person_visit_id
    class Meta:
        db_table = 'person_visit'


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
    address = models.TextField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    visted_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
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

