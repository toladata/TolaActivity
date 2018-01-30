import csv
from django.core.management.base import BaseCommand, CommandError
from indicators.models import *
from django.utils import timezone

class Command(BaseCommand):
    help = """
        Update lop, unit_of_measure, and baseline values of indicators based on a csv file
        """

    def add_arguments(self, parser):
        """
        Help on arguments: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
        """
        parser.add_argument('-f', '--file', action='store', nargs='?', required=True, dest='filepath')


    def handle(self, *args, **options):
        file = options['filepath']
        self.stdout.write(self.style.WARNING('updating indicators for program_id = "%s"' % file))

        with open(file, 'rb') as csvfile:
            indicatorcsv_reader = csv.reader(csvfile)
            # This skips the first row (header) of the CSV file.
            next(indicatorcsv_reader)
            for row in indicatorcsv_reader:
                indicator_id = row[0]
                unit_of_measure = row[4]
                lop = row[5]
                baseline = row[6]
                indicator = None
                try:
                    lop = float(lop) if '.' in lop else int(lop)
                except ValueError as e:
                    self.stdout.write(self.style.ERROR('indicator with id = %s has invalid lop = %s' % (indicator.id, lop) ))
                    continue

                try:
                    baseline = float(baseline) if '.' in baseline else int(baseline)
                except ValueError as e:
                    self.stdout.write(self.style.ERROR('indicator with id = %s has invalid lop = %s' % (indicator.id, baseline) ))
                    continue

                try:
                    indicator = Indicator.objects.get(pk=indicator_id)
                    self.stdout.write(self.style.SUCCESS(indicator.id))
                except Indicator.DoesNotExist as e:
                    self.stdout.write(self.style.ERROR('indicator with id = %s does not exist!' % indicator_id))
                    continue

                try:
                    indicator.unit_of_measure = unit_of_measure
                    indicator.lop_target = lop
                    indicator.baseline = baseline
                    indicator.save()
                except Exception as e:
                    self.stdout.write(self.style.ERROR('failed to save indicator with id = %s' % indicator.id))

