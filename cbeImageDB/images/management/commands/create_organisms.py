from django.core.management.base import BaseCommand
from images.models import Organism
import pandas


class Command(BaseCommand):
    help = "Reads in a list of organisms from a file named organisms.csv and populates the database"

    def _generate_organisms(self):
        csv = pandas.read_csv('organisms/organisms.csv', sep='|')

        print('Total number of organisms to add: {}'.format(len(csv)))
        for index, row in csv.iterrows():
            if index % 5000 == 0 and index != 0:
                print('Added organism number: {}'.format(index))

            Organism.objects.create(storid=row[0], ncbi_id=row[1],
                                    organism_name=row[2])


    def handle(self, *args, **options):
        self._generate_organisms()
