# Generated by Django 3.0.7 on 2020-06-15 23:03

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrences',
            name='geo_location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='occurrences',
            name='category',
            field=models.CharField(choices=[('SPECIAL_EVENT', 'Special Event'), ('INDICENT', 'Incident'), ('WEATHER_CONDITION', 'Weather Condition'), ('ROAD_CONDITION', 'Road Condition')], max_length=500),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]