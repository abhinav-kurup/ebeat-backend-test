# Generated by Django 4.2.4 on 2023-08-12 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_rename_region_beatareamodel_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addeditmodel',
            name='chaing_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]