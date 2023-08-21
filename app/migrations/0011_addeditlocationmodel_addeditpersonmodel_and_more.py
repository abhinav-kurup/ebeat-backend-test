# Generated by Django 4.2.3 on 2023-08-16 16:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_beatofficermodel_tid'),
        ('app', '0010_personmodel_arm_licenses_personmodel_bad_character_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddEditLocationModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('approval_status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default=('PENDING', 'Pending'), max_length=12)),
                ('chaing_id', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='approvals')),
                ('incharge_name', models.CharField(blank=True, max_length=50, null=True)),
                ('incharge_contact', models.CharField(blank=True, max_length=50, null=True)),
                ('incharge_description', models.CharField(blank=True, max_length=50, null=True)),
                ('BO', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bo_req_loc', to='authentication.beatofficermodel')),
            ],
            options={
                'db_table': 'location_approval_requests',
            },
        ),
        migrations.CreateModel(
            name='AddEditPersonModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('approval_status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default=('PENDING', 'Pending'), max_length=12)),
                ('chaing_id', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='approvals')),
                ('arm_licenses', models.BooleanField(blank=True, default=False, null=True)),
                ('bad_character', models.BooleanField(blank=True, default=False, null=True)),
                ('senior_citizen', models.BooleanField(blank=True, default=False, null=True)),
                ('budding_criminals', models.BooleanField(blank=True, default=False, null=True)),
                ('suspected_brothels', models.BooleanField(blank=True, default=False, null=True)),
                ('proclaimed_offenders', models.BooleanField(blank=True, default=False, null=True)),
                ('criminal_of_known_areas', models.BooleanField(blank=True, default=False, null=True)),
                ('externee_more_than_2_crimes', models.BooleanField(blank=True, default=False, null=True)),
                ('BO', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bo_req_per', to='authentication.beatofficermodel')),
                ('beat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edit_person_in_ba', to='authentication.beatareamodel')),
            ],
            options={
                'db_table': 'person_approval_requests',
            },
        ),
        migrations.DeleteModel(
            name='AddEditModel',
        ),
    ]
