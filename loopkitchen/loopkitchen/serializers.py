from rest_framework import serializers
from .models import StoreReport

class ReportSerializer(serializers.Serializer):
    class Meta:
        model = StoreReport
        fields = '__all__'


