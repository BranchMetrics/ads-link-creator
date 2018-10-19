# python 3
from urllib.parse import unquote
from urllib import parse
import csv
import json
import os
import errno
import sys


BASE_URL_COL_NAME = 'base_url'
TEMPLATE_COL_NAME = 'template_name'


class Settings:
    """An object to hold all the data in the settings

    Stores all the data form the settings.json file so it can be accessed globally.

    input_file (str): the filename we want to parse
    output_file (str): the file name we want to write to
    csv_deliminator (str): the delimainator of the values in the input_file
    base_url (str): the base url to append all data to
    templates (List (str)): a list of all the templates
    """

    def __init__(self, input_file=None, output_file=None, csv_deliminator=None, base_url=None, templates=[], templates_folder=None):
        self.input_file = input_file
        self.output_file = output_file
        self.csv_deliminator = csv_deliminator
        self.base_url = base_url
        self.templates_folder = templates_folder
        self.templates = templates
        self.template_data = {}
        self.active_template = ''

    def get_templates(self):
        for x in os.listdir(self.templates_folder):
            self.templates.append(os.path.join(self.templates_folder, x))

        for filename in self.templates:
            with open(filename) as file:
                data = json.load(file)
                self.template_data[os.path.basename(filename).split('.')[0]] = data


settings = Settings()


def merge_dictionaries(row_data, default):
    """Merge d2 into d1, where d1 has priority

    for all values of d2 merge them into d1. If a value exists in d1 and in d2 keep the value from d1

    :param d1: dictionary of values
    :param d2: dictionary of values
    :return: dictionary of unified values
    """
    if default is None:
        return row_data
    if row_data is None:
        return default

    return {**default, **row_data} # this is python 3.5 only



def import_settings():

    if not os.path.isfile('settings.json'):
        # settings file doesn't exist
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'settings.json')

    with open('settings.json') as file:
        data = json.load(file)

        # required attributes, fail if missing
        settings.input_file = os.path.join(os.path.dirname(sys.argv[0]), data['input_folder'], data['input_file'])
        settings.output_file = data['output_file']
        settings.csv_deliminator = data['csv_deliminator']
        settings.base_url = data['base_url']
        settings.templates_folder = os.path.join(os.path.dirname(sys.argv[0]), data['templates_folder'])

        settings.get_templates()


def parse_csv(settings):
    with open(settings.input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=settings.csv_deliminator)
        for row in csv_reader:
            if BASE_URL_COL_NAME not in row:
                raise KeyError("No such key ({}) found in {}".format(BASE_URL_COL_NAME, settings.input_file))

            if settings.base_url is None or settings.base_url == '':
                settings.base_url = row.get(BASE_URL_COL_NAME, None)
                if BASE_URL_COL_NAME in row:
                    del row[BASE_URL_COL_NAME]  # don't need this column for url creation

            if settings.active_template is '':
                settings.active_template = row.get(TEMPLATE_COL_NAME, None)
                if TEMPLATE_COL_NAME in row:
                    del row[TEMPLATE_COL_NAME]  # don't need this column for url creation


            link_data = merge_dictionaries(row, settings.template_data.get(settings.active_template, None))
            # url = settings.base_url + '&'.join(str(x[0]) + '=' + str(x[1]) for x in row.items())
            url = settings.base_url + parse.urlencode(link_data, safe='{}:') # safe characters do not get encoded
            print(url)

if __name__ == '__main__':
    import_settings()
    parse_csv(settings)