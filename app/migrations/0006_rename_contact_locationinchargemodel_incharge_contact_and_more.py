# Generated by Django 4.2.3 on 2023-08-05 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_persontypemodel_personmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationinchargemodel',
            old_name='contact',
            new_name='incharge_contact',
        ),
        migrations.RenameField(
            model_name='locationinchargemodel',
            old_name='description',
            new_name='incharge_description',
        ),
        migrations.RenameField(
            model_name='locationinchargemodel',
            old_name='name',
            new_name='incharge_name',
        ),
    ]
