#!/usr/bin/env python

from parse_candidates import Candidate

CANDIDATES = (
    ('biden', 'nav',  None, 'article', None, False, ('https://joebiden.com/joes-vision/',),),
)

if __name__ == '__main__':
    name, nav_tag, nav_attr, c_tag, c_attr, bad, urls = CANDIDATES[0]
    c = Candidate(name, nav_tag, nav_attr, c_tag, c_attr, bad, urls)
    c.load_pages()
    print c.pages
