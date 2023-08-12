from authentication.models import *
from django.db import models
from base.models import *
from app.models import *


class LoactionVisitModel(BaseVisit):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_location_visit", on_delete=models.PROTECT)
    location = models.ForeignKey(LocationModel, related_name="location_visit", on_delete=models.PROTECT)
    def __str__(self):
        return self.visit_id
    class Meta:
        db_table = 'location_visit'


class PersonVisitModel(BaseVisit):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_person_visit", on_delete=models.PROTECT)
    person = models.ForeignKey(PersonModel, related_name="person_visit", on_delete=models.PROTECT)
    def __str__(self):
        return self.visit_id
    class Meta:
        db_table = 'person_visit'


class SummonWarrentModel(BaseModel):
    class CategoryType(models.TextChoices):
        NOTICE = "NOTICE", "Notice"
        SUMMON = "SUMMON", "Summon"
        WARRENT = "WARRENT", "Warrent"
    class StatusTypes(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SERVED = "SERVED", "Served"
        UNSERVED = "UNSERVED", "Unserved"
    category = models.CharField(max_length=10, choices=CategoryType.choices)
    police_station = models.ForeignKey(PoliceStationModel, related_name="police_station_order", on_delete=models.DO_NOTHING)
    assigned_to = models.ManyToManyField(BeatOfficerModel)
    order_id = models.CharField(max_length=20)
    order_name = models.CharField(max_length=50)
    address = models.TextField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    done_by = models.ForeignKey(BeatOfficerModel, related_name="bo_summ", on_delete=models.DO_NOTHING, null=True, blank=True)
    photo = models.ImageField(upload_to="order", height_field=None, width_field=None, max_length=None)
    comment = models.TextField(null=True, blank=True)
    order_status = models.CharField(max_length=10, choices=StatusTypes.choices)
    visted_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    def __str__(self):
        return self.order_id
    class Meta:
        db_table = 'court_orders'



class BeatOfficerLogs(BaseModel):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_logs", on_delete=models.PROTECT)
    comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.BO.name
    class Meta:
        db_table = 'bo_logs'

