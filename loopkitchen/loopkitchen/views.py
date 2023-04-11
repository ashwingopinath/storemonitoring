from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
import requests
from .models import StoreReport
from .tasks import create_report
import csv

DB_BASE_URL = 'http://127.0.0.1:8000/'

class Report(APIView):
    def get(self, request):
        report_id = request.query_params.get('report_id')
        if not report_id:
            return Response({'error': 'report_id is a required parameter'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            store_report = StoreReport.objects.get(id=report_id)
        except StoreReport.DoesNotExist:
            return Response("Invalid id",status=status.HTTP_404_NOT_FOUND)
        if(store_report.status == 'Running'):
            return Response('Running')
        else:
            response = Response("Complete", content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'
            writer = csv.writer(response)
            writer.writerow(['store_id', 'uptime_last_hour', 'uptime_last_day','update_last_week','downtime_last_hour','downtime_last_day','downtime_last_week'])

            writer.writerow([store_report.store_id, store_report.uptime_last_hour, store_report.uptime_last_day, store_report.uptime_last_week,
                             store_report.downtime_last_hour,store_report.downtime_last_day,store_report.downtime_last_week])
            return response
        
    def post(self, request):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({'error': 'store_id is a required parameter'}, status=status.HTTP_400_BAD_REQUEST)
        print("store ID kitti")
        # current_time = datetime.datetime.utcnow()
        current_time = datetime.datetime.fromisoformat('2023-01-24T06:09:52.424578')
        start_time = current_time - datetime.timedelta(weeks=1)
        parameters = {'store_id':store_id,'start_time':start_time.isoformat(),'end_time':current_time.isoformat()}
        print("Ready to make requests")
        store_status = requests.get(DB_BASE_URL + 'store-status/', params=parameters).json()
        store_working_hours = requests.get(DB_BASE_URL + 'store-hours/', params=parameters).json()
        store_timezone = requests.get(DB_BASE_URL + 'store-time-zone/', params=parameters).json()

        # Create entry in StoreReport
        store_report = StoreReport.objects.create(store_id=store_id,
                                                  status='Running')
        print(store_report)
        # Run in Celery
        create_report(store_report.id, current_time, store_status, store_working_hours, store_timezone)
        return Response(store_report.id)
    

