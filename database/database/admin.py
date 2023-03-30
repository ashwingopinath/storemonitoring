from django.contrib import admin
from .models import StoreHours, StoreStatus, StoreTimeZone

admin.site.register(StoreHours)
admin.site.register(StoreStatus)
admin.site.register(StoreTimeZone)