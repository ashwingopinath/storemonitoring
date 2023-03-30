import csv
import os
from django.core.management.base import BaseCommand
from database.models import StoreHours


class Command(BaseCommand):
    help = 'Uploads store hours from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR('File "{}" does not exist'.format(file_path)))
            return

        with open(file_path) as f:
            reader = csv.reader(f)
            n = 0
            for row in reader:
                if(n==0): 
                    n=1
                    continue
                if n % 100 == 0:
                    print(n)
                _, created = StoreHours.objects.get_or_create(
                    store_id=row[0],
                    day=row[1],
                    start_time_local=row[2],
                    end_time_local=row[3],
                )
                n += 1


