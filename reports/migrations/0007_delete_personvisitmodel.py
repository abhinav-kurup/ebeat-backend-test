# Generated by Django 4.2.3 on 2023-08-16 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_remove_personvisitmodel_person'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PersonVisitModel',
        ),
    ]