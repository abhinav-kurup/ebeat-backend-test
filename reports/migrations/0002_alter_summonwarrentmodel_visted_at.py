# Generated by Django 4.2.4 on 2023-08-07 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summonwarrentmodel',
            name='visted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]