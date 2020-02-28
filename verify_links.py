#!/usr/bin/env python
"""
Make sure all links in candidates.py are in data/changes/**/links and vice versa
"""

import os
from subprocess import Popen, PIPE
import sys

from candidates import CANDIDATES

KEEPERS = set()
SKIPPERS = set()
IGNORED_DUPLICATES = set()

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

def load_duplicates():
    with open ('duplicates') as f:
        for l in f:
            url = l.strip()
            IGNORED_DUPLICATES.add(url)
            if url.endswith('/'):
                IGNORED_DUPLICATES.add(url[0:-1])
            else:
                IGNORED_DUPLICATES.add(url + '/')

def validate_candidate(name, host, candidate_urls):
    links_urls = urls_in_links(name, host)
    missing_urls = urls_not_in_links(candidate_urls, links_urls)
    if missing_urls:
        print('Not in links')
        for url in missing_urls:
            print(url)
    all_missing_links = links_not_in_candidates(candidate_urls, links_urls)
    if all_missing_links:
        samenamed_urls, missing_links = urls_with_duplicate_filenames(candidate_urls, all_missing_links)
        if missing_links:
            print('Not in candidates')
            for link in missing_links:
                print(link)
        if samenamed_urls:
            print('Duplicated filenames')
            for duplicate in samenamed_urls:
                print(duplicate)

def urls_in_links(name, host):
    links = set([host])
    with open('data/changes/{}/links'.format(name)) as f:
        for l in f:
            links.add(l.strip())
    return links

def urls_in_candidates(host, link_bundles):
    candidate_urls = set((host,))
    for tag, attr, bad, urls in link_bundles:
        candidate_urls.update(urls)
    return candidate_urls

def links_not_in_candidates(candidate_urls, links):
    missing_links = set()
    for link in links:
        if link.endswith('/'):
            mod_link = link[0:-1]
        elif link.endswith('/?'):
            mod_link = link[0:-2]
        else:
            mod_link = link + '/'
        if link not in candidate_urls and mod_link not in candidate_urls and link not in SKIPPERS:
            missing_links.add(link)
    return missing_links

def filename_from_url(url):
    return [part for part in url.split('/') if part][-1]

def urls_with_duplicate_filenames(candidate_urls, missing_links):
    duplicates = set()
    still_missing = set()
    filenames_in_candidates = set([filename_from_url(url) for url in candidate_urls])
    for missing_link in missing_links:
        missing_link_filename = filename_from_url(missing_link)
        if missing_link_filename in filenames_in_candidates:
            if missing_link not in IGNORED_DUPLICATES:
                duplicates.add(missing_link)
        else:
            still_missing.add(missing_link)
    return (duplicates, still_missing,)

def urls_not_in_links(candidate_urls, links):
    missing_links = set()
    for candidate_url in candidate_urls:
        if candidate_url not in links and candidate_url not in KEEPERS:
            missing_links.add(candidate_url)
    return missing_links

def run():
    for name, host, link_bundles in CANDIDATES:
        validate_candidate(name, host, urls_in_candidates(host, link_bundles))

def fix():
    to_skip = set()
    to_keep = set()
    accepted_duplicates = set()
    for name, host, link_bundles in CANDIDATES:
        candidate_urls = urls_in_candidates(host, link_bundles)
        links = urls_in_links(name, host)
        to_keep.update(urls_not_in_links(candidate_urls, links))
        all_missing_links = links_not_in_candidates(candidate_urls, links)
        if all_missing_links:
            samenamed_urls, missing_links = urls_with_duplicate_filenames(candidate_urls, all_missing_links)
            to_skip.update(missing_links)
            accepted_duplicates.update(samenamed_urls)
    with open('tokeep', 'a') as f:
        for url in to_keep:
            f.write(url + '\n')
    with open('toskip', 'a') as f:
        for url in to_skip:
            f.write(url + '\n')
    with open('duplicates', 'a') as f:
        for url in accepted_duplicates:
            f.write(url + '\n')

def output_added():
    cmd = ['git',
               'ls-files',
               '--others',
               '--exclude-standard',]
    p = Popen(cmd, stdout=PIPE)
    o = p.communicate()
    files = set()
    for l in o:
        if l:
            for filename in l.strip().split('\n'):
                if os.path.exists(filename):
                    files.add(filename)
    for filename in files:
        with open(filename) as f:
            print('****************************')
            print(filename)
            print('****************************')
            for l in f:
                print(l.strip())

if __name__ == '__main__':
    load_keepers()
    load_skippers()
    load_duplicates()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'a':
            fix()
        elif sys.argv[1] == 'added':
            output_added()
    else:
        run()
