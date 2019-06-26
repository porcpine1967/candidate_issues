#!/usr/bin/env python
import pickle

from parse_candidates import Candidate

CANDIDATES = (
    ('bennet', 'nav', None, 'article', None,),
    ('biden', 'nav',  None, 'article', None,),
    ('booker', 'nav', None,  None, None),
    ('buttigieg', 'nav', ('class', 'nav',), 'div', ('class', 'IssuesMain',),),
    ('castro', 'ul', ('class', 'header__nav',),'div', ('class', 'blog__posts',),),
    ('deblasio', 'ul', ('class', 'header__nav--list',),None, None,),
    ('delaney', 'ul', ('id', 'main-navigation',), 'main', ('id', 'main',),),
    ('delaney2', None, None, 'main', ('id', 'main',),),
    ('gabbard', 'div', ('class', 'main-menus',), 'article', ('class', 's-article',),),
    ('gillibrand', 'nav', ('id', 'nav-header',), 'article', None),
    ('gillibrand2', None, None, 'article', None),
    ('harris', 'nav', ('class', 'primary',), 'div', ('class', 'content',),),
    ('hickenlooper', 'nav', ('class', 'elementor-nav-menu__container',), 'div', ('class', 'elementor-widget-text-editor',),),
)

def pickle_candidates():
    for name, nav_tag, nav_attr, c_tag, c_attr in CANDIDATES:
        c = Candidate(name, nav_tag, nav_attr, c_tag, c_attr)
        c.load_links()
        pickle.dump(c.links, open('%s.links' % name, 'wb'))
        c.load_lines()
        line_file =  open('%s.lines' % name, 'wb')
        for line in c.lines:
            line_file.write("%s\n" % line)
        line_file.close()

def test_candidates():
    for name, nav_tag, nav_attr, c_tag, c_attr in CANDIDATES:
        c = Candidate(name, nav_tag, nav_attr, c_tag, c_attr)
        c.load_links()
        test_links = pickle.load(open('%s.links' % name))
        if test_links != c.links:
            print '%s has unmatching links' % name
            for l in test_links:
                if l not in c.links:
                    print '%s not current' % l
            for l in c.links:
                if l not in test_links:
                    print '%s disappeared' % l
        c.load_lines()
        test_lines = []
        line_file = open('%s.lines' % name)
        for line in line_file:
            test_lines.append(line.strip())
        line_file.close()
        if test_lines != c.lines:
            print '%s has unmatching lines' % name
            for l in test_lines:
                if l not in c.lines:
                    print '%s not current' % l
            for l in c.lines:
                if l not in test_lines:
                    print '%s disappeared' % l
if __name__ == '__main__':
#    pickle_candidates()
    test_candidates()

