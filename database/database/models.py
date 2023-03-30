from django.db import models

class StoreStatus(models.Model):
    store_id = models.BigIntegerField()
    status = models.CharField(max_length=8)
    timestamp_utc = models.DateTimeField()
    

    def __str__(self):
        return f'Store {self.store_id} - Status: {self.status} - Timestamp: {self.timestamp_utc}'


class StoreHours(models.Model):
    store_id = models.BigIntegerField()
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f'Store {self.store_id} - Day: {self.day_of_week} - Hours: {self.start_time_local} to {self.end_time_local}'


class StoreTimeZone(models.Model):
    store_id = models.BigIntegerField()
    timezone_str = models.CharField(max_length=255, default='America/Chicago')

    def __str__(self):
        return f'Store {self.store_id} - Timezone: {self.timezone_str}'