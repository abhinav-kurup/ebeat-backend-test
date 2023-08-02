from django.db import models
from base.models import *


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
