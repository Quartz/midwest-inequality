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
        .group_by('census_region')
        .group_by('size')
        .group_by('year2'))

def aggregate(data):
    aggregated = (data['grouped']
        .aggregate([
            ('total_firms', agate.Sum('Firms')),
            ('total_establishments', agate.Sum('Estabs')),
            ('total_employees', agate.Sum('Emp'))
        ])
    )

    tester = agate.TypeTester(force={
        'year': agate.Text()
    })

    pop_estimates = agate.Table.from_csv('region_pop_lookup.csv', delimiter='\t', column_types=tester)

    data['aggregated'] = aggregated.join(pop_estimates, lambda r: (r['census_region'], r['year2']), lambda r: (r['region'], r['year']))

def results(data):
    data['aggregated'].to_csv('output.csv')

def main():
    loaded = proof.Analysis(load_bds)
    grouped = loaded.then(group_by_state_and_year)
    aggregated = grouped.then(aggregate)
    aggregated.then(results)

    loaded.run()

if __name__ == '__main__':
    main()
