from collections import defaultdict
import csv
import operator

import requests

"""
records = get_records()
addresses = [r['address'] for r in records]
resps = [latlng(a) for a in addresses]
latlngs = [r.json()['results'][0]['geometry']['location'] for r in resps]
"""

GOOGLE_MAPS_KEY = ''

def get_records(filepath='addresses.csv'):
    # First Name,Last Name,Address 1,Address 2,City,State,Zip
    records = []
    with open(filepath) as f:
        reader = csv.reader(f)
        for row in reader:
            records.append({
                    'street': row[2],
                    'city': row[4],
                    'state': row[5],
                    'zip': row[6],
                    'address': ' '.join([row[2], row[4], row[5], row[6]]),
                    })
    for record in records:
        for k, v in record.items():
            if not (k and v):
                print 'barf', record
    return records


def get_counts(records):
    cities = defaultdict(int)
    zips = defaultdict(int)
    for r in records:
        cities[r['city']] += 1
        zips[r['zip']] += 1
    return {'zips': dict(zips), 'cities': dict(cities)}


def print_count(count):
    for k, v in sorted(count.items(), key=operator.itemgetter(1), reverse=True):
        print k, v


def latlng(address, key=GOOGLE_MAPS_KEY):
    return requests.get('https://maps.googleapis.com/maps/api/geocode/json',
            params={'address': address, 'key': key})
