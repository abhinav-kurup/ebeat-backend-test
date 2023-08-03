from django.db import models
from base.models import *

OFFICER_POSTS = (("PI", "PI"), ("DYSP", "DYSP"), ("SP", "SP"), ("IGP", "IGP"))


class BeatOfficerModel(BaseUser):
    service_number = models.CharField(max_length=10)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'beat_officer'


class OfficerModel(BaseUser):
    post = models.CharField(max_length=50, choices=OFFICER_POSTS, null=True, blank=True)
    service_number = models.CharField(max_length=10)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'officer'
