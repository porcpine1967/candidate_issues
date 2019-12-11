#!/usr/bin/env python
from subprocess import Popen, PIPE



if __name__ == '__main__':
    expected = set([
        'data/changes/gabbard/record',
        'data/changes/hickenlooper/reproductive-healthcare',
        'data/changes/hickenlooper/affordable-college',
        'data/changes/hickenlooper/opioids-crisis',
        'data/changes/hickenlooper/trade',
        'data/changes/hickenlooper/healthcare',
        'data/changes/hickenlooper/minimum-wage',
        'data/changes/hickenlooper/entrepreneurship',
        'data/changes/hickenlooper/tax-code',
        'data/changes/hickenlooper/climate-change',
        'data/changes/hickenlooper/rural-economy',
        'data/changes/hickenlooper/gun-violence',
        'data/changes/hickenlooper/criminal-justice',
        'data/changes/hickenlooper/infrastructure',
        'data/changes/klobuchar/policies',
        'data/changes/klobuchar/issues',
        'data/changes/williamson/issues',
        'data/changes/deblasio/billdeblasio.com',
        ])
    cmds = ['find',
                'data/changes',
                '-size',
                '0',]
    p = Popen(cmds, stdout=PIPE)
    o = p.communicate()
    zeros = set(o[0].split())
    new_zeros = zeros - expected
    if new_zeros:
        print('Additional files with no content:')
        for new_zero in new_zeros:
            print('  {}'.format(new_zero))
    else:
        print('OK')


