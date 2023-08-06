import json

import requests
import random


def chose_prams():
    geo_fields = ['bbox', 'propertyName', 'srsName']
    pass


def chose_filter():
    filer = ['date', 'sortBy', 'count', 'count&sortBy']
    return random.choice(filer)


