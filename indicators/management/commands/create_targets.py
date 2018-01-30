import csv
from django.core.management.base import BaseCommand, CommandError
from indicators.models import *
from django.utils import timezone

def get_month_number(month):
    return 3

class Command(BaseCommand):
    help = """
        Setup targets for indicators by reading a CSV file
        """

    def add_arguments(self, parser):
        """
        Help on arguments: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
        """
        parser.add_argument('-f', '--file', action='store', nargs='?', required=True, dest='filepath')


    def handle(self, *args, **options):
        file = options['filepath']
        generated_pt_ids = []
        self.stdout.write(self.style.WARNING('creating targetes for indicators from = "%s"' % file))

        with open(file, 'rb') as csvfile:
            indicatorcsv_reader = csv.reader(csvfile)
            # This skips the first row (header) of the CSV file.
            next(indicatorcsv_reader)

            for row in indicatorcsv_reader:
                indicator_id = row[0]
                target_frequency = row[4]
                month_name = row[5]
                year = row[6]
                numTargets = row[7]
                indicator = None


                # make sure month is valid
                month = get_month_number(month_name)
                if month == None
                    self.stdout.write(self.style.ERROR('indicator with id = %s has invalid month = %s' % (indicator.id, month_name) ))
                    continue

                # make sure year is valid
                try:
                    year = float(year) if '.' in year else int(year)
                except ValueError as e:
                    self.stdout.write(self.style.ERROR('indicator with id = %s has invalid year = %s' % (indicator.id, year) ))
                    continue

                # make sure numTargets is valid
                try:
                    numTargets = float(numTargets) if '.' in numTargets else int(numTargets)
                except ValueError as e:
                    self.stdout.write(self.style.ERROR('indicator with id = %s has invalid numTargets = %s' % (indicator.id, numTargets) ))
                    continue

                # Fetch the indicator
                try:
                    indicator = Indicator.objects.get(pk=indicator_id)
                    self.stdout.write(self.style.SUCCESS(indicator.id))
                except Indicator.DoesNotExist as e:
                    self.stdout.write(self.style.ERROR('indicator with id = %s does not exist!' % indicator_id))
                    continue

                # save changes to the indicator
                try:
                    indicator.target_frequency = target_frequency
                    start_date = '%s-%s-%s' % (year, month, '01')
                    indicator.target_frequency_start = start_date
                    indicator.target_frequency_num_periods = numTargets
                    indicator.save(commit=False) # do not save yet.

                    generatedTargets = generate_periodic_targets(target_frequency, start_date, numTargets, event_name)
                    for pt in generatedTargets:
                        periodic_target,created = PeriodicTarget.objects.update_or_create(\
                            indicator=indicatr, id=pk,\
                            defaults={'period': pt.get('period', ''), 'target': pt.get('target', 0), 'customsort': i,\
                                    'start_date': start_date, 'end_date': end_date, 'edit_date': timezone.now() })

                        if created:
                            periodic_target.create_date = timezone.now()
                            periodic_target.save()
                            generated_pt_ids.append(periodic_target.id)
                except Exception as e:
                    self.stdout.write(self.style.ERROR('failed to save indicator with id = %s' % indicator.id))

