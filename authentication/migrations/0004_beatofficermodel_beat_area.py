# Generated by Django 4.2.3 on 2023-08-07 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_officermodel_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='beatofficermodel',
            name='beat_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bo_of_ba', to='authentication.beatareamodel'),
        ),
    ]
