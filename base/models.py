from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models as gis_models
from .manager import UserManager
from django.db import models
from .validators import *
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class BaseUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=100, unique=True, validators=[validate_email])
    name = models.CharField(max_length=100, validators=[validate_name])
    phone = models.CharField(max_length=13, validators=[validate_phone_no])
    profile_pic = models.ImageField(upload_to="profile", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    service_number = models.CharField(max_length=10)    # unique=True
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email


class BasePolygon(BaseModel):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    contact_no = models.CharField(max_length=50, null=True, blank=True)
    area = gis_models.PolygonField(srid=4326)
    class Meta:
        abstract = True


class BaseVisit(BaseModel):
    audio = models.FileField(upload_to="audio", max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    situation = models.FloatField(default=5.0, validators=[MaxValueValidator(10.0), MinValueValidator(1.0)])
    img = models.ImageField(upload_to="visit", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    visit_id = models.CharField(max_length=40, unique=True)
    class Meta:
        abstract = True
