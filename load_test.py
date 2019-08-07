#!/usr/bin/env python

import re
import urllib2

SEC_PATTERN = re.compile(r'email-protection#[a-f0-9]+')

CANDIDATES = (
    ('bennet', 'https://michaelbennet.com/vision/drive-economic-opportunity/',),
    ('biden', 'https://joebiden.com/joes-vision/',),
    ('biden2', 'https://joebiden.com/justice/,'),
    ('biden3', 'https://joebiden.com/healthcare/,'),
    ('booker', 'https://corybooker.com/issues/',),
    ('buttigieg', 'https://peteforamerica.com/issues/',),
    ('castro', 'https://issues.juliancastro.com/people-first-immigration',),
    ('deblasio', 'https://billdeblasio.com/policies/',),
    ('delaney', 'https://www.johndelaney.com/issues/cybersecurity/',),
    ('gabbard', 'https://www.tulsi2020.com/record/strengthen-social-security',),
    ('gillibrand', 'https://kirstengillibrand.com/issues/values/',),
    ('harris', 'https://kamalaharris.org/issues/',),
    ('hickenlooper', 'https://www.hickenlooper.com/issues/',),
    ('inslee', 'https://jayinslee.com/issues/100clean',),
    ('klobuchar', 'https://amyklobuchar.com/issues/health-care/',),
    ('orourke', 'https://betoorourke.com/climate-change/iowa/',),
    ('ryan', 'https://timryanforamerica.com/issues/',),
    ('ryan2', 'https://timryanforamerica.com/veterans/',),
    ('sanders', 'https://berniesanders.com/issues/criminal-justice-reform/',),
    ('warren', 'https://elizabethwarren.com/issues',),
    ('williamson', 'https://www.marianne2020.com/issues/climate-change',),
    ('yang', 'https://www.yang2020.com/policies/the-freedom-dividend/',),
)

def load_test_files():
    for name, url in CANDIDATES:
        try:
            req = urllib2.Request(url)
            req.add_header('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
            web = urllib2.urlopen(req)
            f = open('data/test/%s.html' % name, 'wb')
            for l in web:
                f.write(re.sub(SEC_PATTERN, 'email-protection', l))
            f.close()
            web.close()
        except StandardError as e:
            print name, e

if __name__ == '__main__':
    load_test_files()
