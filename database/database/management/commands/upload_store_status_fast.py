import csv
import os
import datetime
import pytz
import django
django.setup()
from django.core.management.base import BaseCommand
from database.models import StoreStatus
from multiprocessing import Pool, cpu_count
from itertools import islice

def localize_timestamp(timestamp_utc):
    return pytz.UTC.localize(timestamp_utc)

def create_store_status(row):
    try:
        timestamp_utc = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f %Z')
    except ValueError:
        timestamp_utc = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S %Z')
    timestamp_utc = localize_timestamp(timestamp_utc)
    return StoreStatus(
        store_id=row[0],
        status=row[1],
        timestamp_utc=timestamp_utc,
    )

def upload_store_status_csv(file_path):
    print("Gonna open file")
    print(file_path)
    with open(file_path) as f:
        reader = csv.reader(f)
        header = list(islice(reader, 1))[0] # skip the header row
        rows = [row for row in reader]
    print("Finished reading file")

    pool = Pool(processes=cpu_count())
    print(f"Initialized pool : {pool}")
    store_statuses = pool.map(create_store_status, rows)
    print("Created store statuses")
    StoreStatus.objects.bulk_create(store_statuses)
    print("Finished uploading store statuses")


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
