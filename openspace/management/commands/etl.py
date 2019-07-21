from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
import pandas as pd

from openspace.models import Space


def extract(file_path):
    df = pd.read_excel(file_path, headers=1)
    return df[df["_Geolocation_latitude"].notnull()].iloc[:, 2:6]


def load(data):
    model_instances = [Space(
        name=row[0],
        location=Point(row[3], row[2], srid=4326),
    ) for row in data.values.tolist()]
    Space.objects.bulk_create(model_instances)


class Command(BaseCommand):
    help = 'Imports existing data from excel'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path']
        data = extract(file_path)
        load(data)
        self.stdout.write(self.style.SUCCESS('Successfully loaded data poll '))
