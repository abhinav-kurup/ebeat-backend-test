from django.contrib.gis.db import models as gis_models
from base.models import BaseModel
from django.db import models



class LocationCategoryModel(BaseModel):
    location_type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
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
        return self.incharge_name
    class Meta:
        db_table = 'location_incharge'


class PersonTypeModel(BaseModel):
    person_type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.person_type
    class Meta:
        db_table = 'person_type'


class PersonModel(BaseModel):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(PersonTypeModel, related_name="person_category", on_delete=models.CASCADE)
    location = gis_models.PointField(srid=4326)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="person", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def _str_(self):
        return self.name
    class Meta:
        db_table = 'person'