import csv
import os
import datetime
import pytz
from django.core.management.base import BaseCommand
from database.models import StoreStatus


def upload_store_status_csv(file_path):
    print("Gonna open file")
    print(file_path)
    with open(file_path) as f:
        reader = csv.reader(f)
        n = 0
        for row in reader:
            if(n==0): 
                n=1
                continue
            if n % 100 == 0:
                print(n)
            timestamp_utc = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f %Z')
            timestamp_utc = pytz.UTC.localize(timestamp_utc)
            _, created = StoreStatus.objects.get_or_create(
                store_id=row[0],
                status=row[1],
                timestamp_utc=timestamp_utc,
            )
            n += 1


class Command(BaseCommand):
    help = 'Uploads store status from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR('File "{}" does not exist'.format(file_path)))
            return

        upload_store_status_csv(file_path)
