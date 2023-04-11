from django.db import models

class StoreReport(models.Model):
    store_id = models.BigIntegerField()
    status = models.CharField(max_length=8)
    uptime_last_hour = models.FloatField(null=True)
    downtime_last_hour = models.FloatField(null=True)
    uptime_last_day = models.FloatField(null=True)
    downtime_last_day = models.FloatField(null=True)
    uptime_last_week = models.FloatField(null=True)
    downtime_last_week = models.FloatField(null=True)

    
    