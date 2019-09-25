#!/usr/bin/env python

import os
import sys

from candidates import CANDIDATES
from parse_candidates import Candidate

class CandidatesManager(object):
    def __init__(self):
        candidates = {}
        self.working_dir = ''

    def write_candidate_links(self, c):
        with open('{}/links'.format(self.working_dir), 'wb') as f:
            for link in sorted(list(c.links)):
                f.write(link)
                f.write('\n')

    def write_candidate_pages(self, c):
        for page in c.pages:
            with open('{}/{}'.format(self.working_dir, page['filename']), 'wb') as f:
                for line in page['lines']:
                    f.write(line)
                    f.write('\n')

    def load_candidate(self, c):
        c.load_pages()
        self.working_dir = '{}/data/changes/{}'.format(os.path.dirname(os.path.realpath(__file__)), c.name)
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)
        self.write_candidate_links(c)
        self.write_candidate_pages(c)

    def load_candidates(self, index=-1):
        found = False
        for name, host, link_bundles in CANDIDATES:
            print name
            if len(sys.argv) > 1:
                for i in xrange(1, len(sys.argv)):
                    if name == sys.argv[i]:
                        c = Candidate(name, host, link_bundles)
                        found = True
                        self.load_candidate(c)
            else:
                c = Candidate(name, host, link_bundles)
                self.load_candidate(c)
        if len(sys.argv) > 1 and not found:
            print 'No such candidate', sys.argv[1]
            sys.exit(1)

if __name__ == '__main__':
    cm = CandidatesManager()
    cm.load_candidates()
