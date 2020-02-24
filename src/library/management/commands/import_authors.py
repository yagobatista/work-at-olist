from django.core.management.base import BaseCommand, CommandError
from library.models import Author


class Command(BaseCommand):
    help = 'Import data from authors'

    def add_arguments(self, parser):
        parser.add_argument('sheet_name', nargs='+', type=str)

    def handle(self, *args, **options):
        sheet_name = options.get('sheet_name')[0]
        import csv
        authors = []
        with open(sheet_name, 'rb') as f:
            r = csv.reader(f)
            for row in r:
                authors.append(Author(row))
        
        Author.objects.bulk_create()
