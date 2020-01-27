#!/usr/bin/env python
"""
Make sure all links in candidates.py are in data/changes/**/links and vice versa
"""
import sys

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
    links = candidate_links(name, host)
    for url in not_in_urls(urls, links):
        print(url + ' not in ' + name + '/links')
    for link in not_in_links(urls, links):
        print(link + ' not in candidates')

def candidate_links(name, host):
    links = set([host])
    with open('data/changes/{}/links'.format(name)) as f:
        for l in f:
            links.add(l.strip())
    return links

def candidate_urls(host, link_bundles):
    curls = set((host,))
    for tag, attr, bad, urls in link_bundles:
        curls.update(urls)
    return curls

def not_in_links(urls, links):
    missing_links = set()
    for link in links:
        if link.endswith('/'):
            mod_link = link[0:-1]
        else:
            mod_link = link + '/'
        if link not in urls and mod_link not in urls and link not in SKIPPERS:
            missing_links.add(link)
    return missing_links

def not_in_urls(urls, links):
    missing_urls = set()
    for url in urls:
        if url not in links and url not in KEEPERS:
            missing_urls.add(url)
    return missing_urls

def run():
    for name, host, link_bundles in CANDIDATES:
        validate_candidate(name, host, candidate_urls(host, link_bundles))

def fix():
    missing_links = set()
    missing_urls = set()
    for name, host, link_bundles in CANDIDATES:
        urls = candidate_urls(host, link_bundles)
        links = candidate_links(name, host)
        missing_urls.update(not_in_urls(urls, links))
        missing_links.update(not_in_links(urls, links))
    with open('tokeep', 'a') as f:
        for url in missing_urls:
            f.write(url + '\n')
    with open('toskip', 'a') as f:
        for url in missing_links:
            f.write(url + '\n')

if __name__ == '__main__':
    load_keepers()
    load_skippers()
    if len(sys.argv) > 1 and sys.argv[1] == 'a':
        fix()
    else:
        run()
