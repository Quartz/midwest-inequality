#!/usr/bin/env python

import agate
import proof

def load_bds(data):
    tester = agate.TypeTester(force={
        'year2': agate.Text(),
        'state': agate.Text()
    })

    bds = agate.Table.from_csv('bds_e_szst_release.csv', column_types=tester)

    tester = agate.TypeTester(force={
        'fips': agate.Text()
    })

    fips_lookup = agate.Table.from_csv('fips_lookup.csv', column_types=tester)

    data['bds'] = bds.join(fips_lookup, 'state', 'fips')

def group_by_state_and_year(data):
    data['grouped'] = (data['bds']
        .group_by('state_name')
        .group_by('year2'))

def nebraska(data):
    ne = data['grouped']['Nebraska']['2005']

    print(ne)

if __name__ == '__main__':
    loaded = proof.Analysis(load_bds)
    grouped = loaded.then(group_by_state_and_year)
    grouped.then(nebraska)

    loaded.run()
