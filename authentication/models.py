from django.db import models
from base.models import *



class OfficerModel(BaseUser):
    class PolicePost(models.TextChoices):
        SP = "SP", "Superintendent of Police"
        DYSP = "DYSP", "Deputy Superintendent of Police"
        PI = "PI", "Police Inspector"
        IGP = "IGP", "Inspector-General of Police"
    post = models.CharField(max_length=50, choices=PolicePost.choices)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'officer'
        permissions = [
            ("guardian_view_location", "obj level view location permission"),
        ]


class StateModel(BasePolygon):
    igp = models.OneToOneField(OfficerModel, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'state'


class DistrictModel(BasePolygon):
    sp = models.OneToOneField(OfficerModel, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(StateModel, related_name="districts", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'district'


class SubDivisionModel(BasePolygon):
    dysp = models.OneToOneField(OfficerModel, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(DistrictModel, related_name="sub_divisions", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'sub_division'


class PoliceStationModel(BasePolygon):
    pi = models.OneToOneField(OfficerModel, on_delete=models.SET_NULL, null=True, blank=True)
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
    beat_area = models.ForeignKey(BeatAreaModel, related_name="bo_of_ba", on_delete=models.SET_NULL, null=True, blank=True)
    tid = models.CharField(max_length=10)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'beat_officer'


class TempAssignmentModel(BaseModel):
    officer = models.ForeignKey(OfficerModel, related_name="officer_temp_assignment", on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=50)
    def __str__(self):
        return self.officer.email
    class Meta:
        db_table = 'officer_temp_assignmet'

