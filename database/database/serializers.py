from django.db import models
from rest_framework import serializers
from .models import StoreStatus, StoreHours, StoreTimeZone

class StoreStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreStatus
        fields = '__all__'


class StoreHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreHours
        fields = '__all__'


class StoreTimeZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreTimeZone
        fields = '__all__'