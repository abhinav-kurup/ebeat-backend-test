# Generated by Django 4.2.3 on 2023-08-05 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_type_locationmodel_loc_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationmodel',
            old_name='loc_type',
            new_name='type',
        ),
    ]
