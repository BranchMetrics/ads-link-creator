# python 3
from urllib.parse import unquote
from urllib import parse
import csv
import json
import os
import errno


BASE_URL_COL_NAME = 'base_url'


class Settings:
    """An object to hold all the data in the settings

    Stores all the data form the settings.json file so it can be accessed globally.

    input_file (str): the filename we want to parse
    output_file (str): the file name we want to write to
    csv_deliminator (str): the delimainator of the values in the input_file
    base_url (str): the base url to append all data to
    default_templates (List (str)): a list of all the default templates
    """

    def __init__(self, input_file=None, output_file=None, csv_deliminator=None, base_url=None, default_templates=[]):
        self.input_file = input_file
        self.output_file = output_file
        self.csv_deliminator = csv_deliminator
        self.base_url = base_url
        self.default_templates = default_templates


settings = Settings()


def import_settings():

    if not os.path.isfile('settings.json'):
        # settings file doesn't exist
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'settings.json')

    with open('settings.json') as file:
        data = json.load(file)

        # required attributes, fail if missing
        settings.input_file = os.path.join(data['input_folder'], data['input_file'])
        settings.output_file = data['output_file']
        settings.csv_deliminator = data['csv_deliminator']
        settings.base_url = data['base_url']


def parse_csv(settings):
    with open(settings.input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=settings.csv_deliminator)
        for row in csv_reader:
            if BASE_URL_COL_NAME not in row:
                raise KeyError("No such key ({}) found in {}".format(BASE_URL_COL_NAME, settings.input_file))

            if settings.base_url is None or settings.base_url == '':
                settings.base_url = row[BASE_URL_COL_NAME]

            del row[BASE_URL_COL_NAME]  # don't need this column for url creation
            # url = settings.base_url + '&'.join(str(x[0]) + '=' + str(x[1]) for x in row.items())
            url = settings.base_url + parse.urlencode(row, safe='{}:') # safe characters do not get encoded
            print(url)

if __name__ == '__main__':
    import_settings()
    parse_csv(settings)