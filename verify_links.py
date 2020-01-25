#!/usr/bin/env python
"""
Make sure all links in candidates.py are in data/changes/**/links and vice versa
"""
from candidates import CANDIDATES

KEEPERS = set()
SKIPPERS = set()

def load_keepers():
    with open ('tokeep') as f:
        for l in f:
            url = l.strip()
            KEEPERS.add(url)
            if url.endswith('/'):
                KEEPERS.add(url[0:-1])
            else:
                KEEPERS.add(url + '/')

def load_skippers():
    with open ('toskip') as f:
        for l in f:
            url = l.strip()
            SKIPPERS.add(url)
            if url.endswith('/'):
                SKIPPERS.add(url[0:-1])
            else:
                SKIPPERS.add(url + '/')

def validate_candidate(name, host, urls):
    links = set([host])
    with open('data/changes/{}/links'.format(name)) as f:
        for l in f:
            links.add(l.strip())
    for url in urls:
        if url not in links and url not in KEEPERS:
            print(url + ' not in ' + name + '/links')
    for link in links:
        if link.endswith('/'):
            mod_link = link[0:-1]
        else:
            mod_link = link + '/'
        if link not in urls and mod_link not in urls and link not in SKIPPERS:
            print(link + ' not in candidates')

if __name__ == '__main__':
    load_keepers()
    load_skippers()
    for name, host, link_bundles in CANDIDATES:
        candidate_urls = set((host,))
        for tag, attr, bad, urls in link_bundles:
            candidate_urls.update(urls)
        validate_candidate(name, host, candidate_urls)
