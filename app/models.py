from django.contrib.gis.db import models as gis_models
from base.models import BaseModel
from django.db import models
from authentication.models import BeatAreaModel, BeatOfficerModel



class LocationCategoryModel(BaseModel):
    location_type = models.CharField(max_length=50)
    def __str__(self):
        return self.location_type
    class Meta:
        db_table = 'location_type'


class LocationModel(BaseModel):
    name = models.CharField(max_length=50)
    location = gis_models.PointField(srid=4326)
    type = models.ForeignKey(LocationCategoryModel, related_name="location_category", on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="locations", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'locations'


class LocationInchargeModel(BaseModel):
    location = models.ForeignKey(LocationModel, related_name="location_incharge", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'location_incharge'


class PersonModel(BaseModel):
    name = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="person", height_field=None, width_field=None, max_length=None)
    description = models.TextField(null=True, blank=True)
    beat = models.ForeignKey(BeatAreaModel, related_name="person_in_ba", on_delete=models.CASCADE)
    arm_licenses = models.BooleanField(default=False)
    bad_character = models.BooleanField(default=False)
    senior_citizen = models.BooleanField(default=False)
    budding_criminals = models.BooleanField(default=False)
    suspected_brothels = models.BooleanField(default=False)
    proclaimed_offenders = models.BooleanField(default=False)
    criminal_of_known_areas = models.BooleanField(default=False)
    externee_more_than_2_crimes = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'person'


class AddEditModel(BaseModel):
    class ApprovalForType(models.TextChoices):
        LOCATION = "LOCATION", "Location"
        PERSON = "PERSON", "Person"
    class NewApproval(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
    approval_type = models.CharField(max_length=12, choices=ApprovalForType.choices)
    approval_status = models.CharField(max_length=12, choices=NewApproval.choices, default=NewApproval.choices[0])
    chaing_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="approvals", null=True, blank=True, max_length=None)
    incharge_name = models.CharField(max_length=50, null=True, blank=True)
    incharge_contact = models.CharField(max_length=50, null=True, blank=True)
    incharge_description = models.CharField(max_length=50, null=True, blank=True)
    BO = models.ForeignKey(BeatOfficerModel, related_name="bo_req", on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'approval_requests'
