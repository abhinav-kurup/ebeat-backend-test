# Generated by Django 4.2.3 on 2023-08-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_alter_generalvisitmodel_visit_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summonwarrentmodel',
            name='visted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
