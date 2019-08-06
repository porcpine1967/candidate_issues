#!/usr/bin/env python
import pickle
import sys

from candidates import CANDIDATES
from parse_candidates import Candidate

def pickle_candidates():
    for name, host, c_tag, c_attr, bad, _ in CANDIDATES:
        c = Candidate(name, host, c_tag, c_attr, bad)
        c.load_links()
        pickle.dump(c.links, open('data/test/%s.links' % name, 'wb'))
        c.load_lines()
        line_file =  open('data/test/%s.lines' % name, 'wb')
        for line in c.lines:
            line_file.write("%s\n" % line)
        line_file.close()

def test_candidates():
    search = len(sys.argv) > 1 and sys.argv[1] != 'p'
    found = False
    for name, host, c_tag, c_attr, bad, _ in CANDIDATES:
        if search and name != sys.argv[1]:
            print 'skipping', name
            continue
        found = True
        c = Candidate(name, host, c_tag, c_attr, bad)
        c.load_links()
        test_links = pickle.load(open('data/test/%s.links' % name))
        if test_links != c.links:
            print '%s has unmatching links' % name
            for l in test_links:
                if l not in c.links:
                    print '%s disappeared' % l
            for l in c.links:
                if l not in test_links:
                    print '%s new' % l
        c.load_lines()
        test_lines = []
        line_file = open('data/test/%s.lines' % name)
        for line in line_file:
            test_lines.append(line.strip())
        line_file.close()
        if test_lines != c.lines:
            print '%s has unmatching lines' % name
            ctr = 0
            for l in test_lines:
                if l not in c.lines:
                    ctr += 1
            if ctr:
                print ' {} lines missing'.format(ctr)
            ctr = 0
            for l in c.lines:
                if l not in test_lines:
                    ctr += 1
            if ctr:
                print ' {} new lines'.format(ctr)
    if search and not found:
        print 'no such candidate', sys.argv[1]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'p':
        pickle_candidates()
    test_candidates()

