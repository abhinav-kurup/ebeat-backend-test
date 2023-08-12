from django.db import models


class IGPManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post="IGP")


class SPManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post="SP")


class DYSPManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post="DYSP")


class PIManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post="PI")



    # admin_objects = models.Manager()
    # igp_objects = IGPManager()
    # sp_objects = SPManager()
    # dysp_objects = DYSPManager()
    # pi_objects = PIManager()