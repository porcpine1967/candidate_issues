#!/usr/bin/env python
"""
Make sure all links in candidates.py are in data/changes/**/links
"""
from candidates import CANDIDATES

def validate_candidate(name, host, urls):
    links = set([host])
    with open('data/changes/{}/links'.format(name)) as f:
        for l in f:
            links.add(l.strip())
    for url in urls:
        if url not in links:
            print(name, url)

if __name__ == '__main__':
    candidate_links = {}
    for name, host, link_bundles in CANDIDATES:
        candidate_urls = set()
        candidate_links[name] = candidate_urls
        for tag, attr, bad, urls in link_bundles:
            for url in urls:
                candidate_urls.add(url)
        validate_candidate(name, host, urls)
