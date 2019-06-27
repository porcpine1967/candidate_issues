#!/usr/bin/env python

import re
import urllib2

SEC_PATTERN = re.compile(r'#[a-f0-9]{46}')

CANDIDATES = (
    ('bennet', 'https://michaelbennet.com/vision/drive-economic-opportunity/',),
    ('biden', 'https://joebiden.com/joes-vision/',),
    ('booker', 'https://corybooker.com/issues/',),
    ('booker2', 'https://corybooker.com/issues/criminal-justice/',),
    ('buttigieg', 'https://peteforamerica.com/issues/',),
    ('castro', 'https://www.julianforthefuture.com/',),
    ('deblasio', 'https://billdeblasio.com/',),
    ('delaney', 'https://www.johndelaney.com/issues/',),
    ('delaney2', 'https://www.johndelaney.com/issues/infrastructure/',),
    ('gabbard', 'https://www.tulsi2020.com/about',),
    ('gillibrand', 'https://kirstengillibrand.com/issues/'),
    ('gillibrand2', 'https://kirstengillibrand.com/issues/values/',),
    ('harris', 'https://kamalaharris.org/meet-kamala/',),
    ('hickenlooper', 'https://www.hickenlooper.com/issues/',),
    ('inslee', 'https://jayinslee.com/issues',),
    ('inslee2', 'https://jayinslee.com/issues/100clean',),
    ('klobuchar', 'https://amyklobuchar.com/issues/health-care/',),
    ('orourke', 'https://betoorourke.com/kickoff-remarks/',),
    ('ryan', 'https://timryanforamerica.com/issues/',),
    ('sanders', 'https://berniesanders.com/issues/',),
    ('sanders2', 'https://berniesanders.com/issues/health-care-for-all/',),
    ('swalwell', 'https://ericswalwell.com/my-plan/',),
    ('warren', 'https://elizabethwarren.com/issues',),
    ('williamson', 'https://www.marianne2020.com/issues',),
    ('williamson2', 'https://www.marianne2020.com/issues/child-advocacy',),
    ('yang', 'https://www.yang2020.com/policies/',),
    ('yang2', 'https://www.yang2020.com/policies/the-freedom-dividend/',),
)

def load_test_files():
    for name, url in CANDIDATES:
        try:
            req = urllib2.Request(url)
            req.add_header('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
            web = urllib2.urlopen(req)
            f = open('%s.html' % name, 'wb')
            for l in web:
                f.write(re.sub(SEC_PATTERN, '', l))
            f.close()
            web.close()
        except StandardError as e:
            print name, e

if __name__ == '__main__':
    load_test_files()
