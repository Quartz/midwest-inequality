#!/usr/bin/env python

import agate
import requests

def main():
    states = agate.Table.from_csv('fips_lookup.csv')

    for usps in states.columns['usps'].values():
        print(usps)

        data = requests.get('http://www.aflcio.org/apps/paywatch2014/paywatch_state.php?state=%s' % usps)

        with open('paywatch/%s.json' % usps, 'w') as f:
            f.write(data.text)

if __name__ == '__main__':
    main()
