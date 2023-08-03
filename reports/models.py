from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import BeatOfficerModel
from base.models import BaseModel
from django.db import models
from app.models import *


class LoactionVisit(BaseModel):
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_report", on_delete=models.CASCADE)
    location = models.ForeignKey(LocationModel, on_delete=models.CASCADE)
    audio = models.FileField(upload_to="audio", max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to="location_visit", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    situation = models.FloatField(default=5.0, validators=[MaxValueValidator(10.0), MinValueValidator(0.0)])
    report_id = models.CharField(max_length=50)
    def __str__(self):
        return self.report_id


# class PersonVisit(BaseModel):
