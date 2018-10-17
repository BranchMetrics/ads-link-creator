# python 3
from urllib.parse import unquote
import csv
import json
import os
import errno




class Settings:

    def __init__(self, input_file=None, output_file=None, csv_deliminator=None):
        self.input_file = input_file
        self.output_file = output_file
        self.csv_deliminator = csv_deliminator

settings = Settings()

def import_settings():

    if not os.path.isfile('settings.json'):
        # settings file doesn't exist
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'settings.json')

    with open('settings.json') as file:
        data = json.load(file)

        settings.input_file = os.path.join(data['input_folder'], data['input_file'])
        settings.output_file = data['output_file']
        settings.csv_deliminator = data['csv_deliminator']


def parse_csv(settings):
    with open(settings.input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=settings.csv_deliminator)
        for row in csv_reader:
            print(row)
            # '&'.join( str(x[0]) + '=' + str(x[1]) for x in row.items())

if __name__ == '__main__':
    import_settings()
    parse_csv(settings)