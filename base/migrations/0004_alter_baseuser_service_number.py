# Generated by Django 4.2.4 on 2023-08-11 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_baseuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='service_number',
            field=models.CharField(default='abc', max_length=10),
        ),
    ]
