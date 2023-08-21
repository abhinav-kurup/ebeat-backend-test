# Generated by Django 4.2.3 on 2023-08-16 16:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_beatofficermodel_tid'),
        ('app', '0010_personmodel_arm_licenses_personmodel_bad_character_and_more'),
        ('reports', '0007_delete_personvisitmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonVisitModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio')),
                ('comments', models.TextField(blank=True, null=True)),
                ('situation', models.FloatField(default=5.0, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(1.0)])),
                ('img', models.ImageField(blank=True, null=True, upload_to='visit')),
                ('visit_id', models.CharField(max_length=40, unique=True)),
                ('BO', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bo_person_visit', to='authentication.beatofficermodel')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_visit', to='app.personmodel')),
            ],
            options={
                'db_table': 'person_visit',
            },
        ),
    ]