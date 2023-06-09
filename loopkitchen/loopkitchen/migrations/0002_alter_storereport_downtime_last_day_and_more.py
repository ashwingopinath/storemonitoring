# Generated by Django 4.1.7 on 2023-04-03 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loopkitchen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storereport',
            name='downtime_last_day',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='storereport',
            name='downtime_last_hour',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='storereport',
            name='downtime_last_week',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='storereport',
            name='uptime_last_day',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='storereport',
            name='uptime_last_hour',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='storereport',
            name='uptime_last_week',
            field=models.FloatField(null=True),
        ),
    ]
