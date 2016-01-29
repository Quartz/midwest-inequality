#!/usr/bin/env python

from collections import OrderedDict
import csv
import glob
import json

def main():
    companies = []

    for path in glob.glob('paywatch/*.json'):
        print(path)

        with open(path) as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        companies.extend(data['data']['companies'])

    with open('paywatch.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=companies[0].keys())
        writer.writeheader()
        writer.writerows(companies)

if __name__ == '__main__':
    main()
