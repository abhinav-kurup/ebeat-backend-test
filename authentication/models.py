from django.db import models
from base.models import *


class BeatOfficerModel(BaseUser):
    service_number = models.CharField(max_length=10)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'beat_officer'


class OfficerModel(BaseUser):
    class PolicePost(models.TextChoices):
        SP = "SP", "Superintendent of Police"
        DYSP = "DYSP", "Deputy Superintendent of Police"
        PI = "PI", "Police Inspector"
        IGP = "IGP", "Inspector-General of Police"
    post = models.CharField(max_length=50, choices=PolicePost.choices)
    service_number = models.CharField(max_length=10)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'officer'
