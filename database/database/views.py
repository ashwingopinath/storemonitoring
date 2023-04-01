from django.db.models import Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StoreStatus, StoreHours, StoreTimeZone
from .serializers import StoreStatusSerializer, StoreHoursSerializer, StoreTimeZoneSerializer


class StoreStatusByTimeAndStoreId(APIView):
    def get(self, request):
        start_time_str = request.query_params.get('start_time')
        end_time_str = request.query_params.get('end_time')
        store_id = request.query_params.get('store_id')

        if not start_time_str or not end_time_str or not store_id:
            return Response({'error': 'start_time, end_time and store_id are required parameters'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            start_time = timezone.datetime.fromisoformat(start_time_str)
            print(start_time)
            end_time = timezone.datetime.fromisoformat(end_time_str)
            print(end_time)
        except ValueError:
            return Response({'error': 'start_time and end_time should be in ISO format'},
                            status=status.HTTP_400_BAD_REQUEST)

        store_statuses = StoreStatus.objects.filter(
            store_id=store_id,
            timestamp_utc__gte=start_time,
            timestamp_utc__lte=end_time
        )
        serializer = StoreStatusSerializer(store_statuses, many=True)
        return Response(serializer.data)


class StoreHoursByStoreId(APIView):
    def get(self, request):
        store_id = request.query_params.get('store_id')

        if not store_id:
            return Response({'error': 'store_id is a required parameter'}, status=status.HTTP_400_BAD_REQUEST)

        store_hours = StoreHours.objects.filter(store_id=store_id)
        serializer = StoreHoursSerializer(store_hours, many=True)
        return Response(serializer.data)


class StoreTimeZoneByStoreId(APIView):
    def get(self, request):
        store_id = request.query_params.get('store_id')

        if not store_id:
            return Response({'error': 'store_id is a required parameter'}, status=status.HTTP_400_BAD_REQUEST)

        store_time_zone = StoreTimeZone.objects.filter(store_id=store_id)
        serializer = StoreTimeZoneSerializer(store_time_zone, many=True)
        return Response(serializer.data)
