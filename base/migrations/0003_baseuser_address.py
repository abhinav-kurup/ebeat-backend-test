# Generated by Django 4.2.4 on 2023-08-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_baseuser_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]