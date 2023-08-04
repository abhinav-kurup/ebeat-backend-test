# Generated by Django 4.2.4 on 2023-08-04 07:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('authentication', '0003_alter_officermodel_managers'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeatOfficerLogs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('BO', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bo_logs', to='authentication.beatofficermodel')),
            ],
            options={
                'db_table': 'bo_logs',
            },
        ),
        migrations.CreateModel(
            name='GeneralVisitModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio')),
                ('comments', models.TextField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='visit')),
                ('visit_id', models.CharField(max_length=25, unique=True)),
                ('visit_to', models.CharField(max_length=50)),
                ('BO', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bo_visit', to='authentication.beatofficermodel')),
            ],
            options={
                'db_table': 'general_visit',
            },
        ),
        migrations.CreateModel(
            name='LoactionVisitModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio')),
                ('comments', models.TextField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='visit')),
                ('visit_id', models.CharField(max_length=25, unique=True)),
                ('situation', models.FloatField(default=5.0, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)])),
                ('BO', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bo_location_visit', to='authentication.beatofficermodel')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.locationmodel')),
            ],
            options={
                'db_table': 'location_visit',
            },
        ),
        migrations.CreateModel(
            name='PersonVisitModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio')),
                ('comments', models.TextField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='visit')),
                ('visit_id', models.CharField(max_length=25, unique=True)),
                ('BO', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bo_person_visit', to='authentication.beatofficermodel')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.personmodel')),
            ],
            options={
                'db_table': 'person_visit',
            },
        ),
        migrations.CreateModel(
            name='SummonWarrentModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.CharField(choices=[('Summon', 'Summon'), ('Warrent', 'Warrent')], max_length=50)),
                ('order_id', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('due_date', models.DateField()),
                ('visted_at', models.DateTimeField(null=True)),
                ('is_visited', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assigned_bo', to='authentication.beatofficermodel')),
                ('police_station', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='police_station_order', to='authentication.policestationmodel')),
            ],
            options={
                'db_table': 'summon_warrent',
            },
        ),
        migrations.DeleteModel(
            name='LoactionVisit',
        ),
    ]
