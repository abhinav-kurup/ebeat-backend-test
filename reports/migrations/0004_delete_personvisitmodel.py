# Generated by Django 4.2.3 on 2023-08-05 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_remove_personvisitmodel_person'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PersonVisitModel',
        ),
    ]
