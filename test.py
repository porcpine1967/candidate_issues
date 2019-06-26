#!/usr/bin/env python
import pickle

from parse_candidates import Candidate

CANDIDATES = (
    ('bennet', 'nav', None, 'article', None, False,),
    ('biden', 'nav',  None, 'article', None, False,),
    ('booker', 'nav', None,  None, None, False,),
    ('buttigieg', 'nav', ('class', 'nav',), 'div', ('class', 'IssuesMain',), False,),
    ('castro', 'ul', ('class', 'header__nav',),'div', ('class', 'blog__posts',), False,),
    ('deblasio', 'ul', ('class', 'header__nav--list',),None, None, False,),
    ('delaney', 'ul', ('id', 'main-navigation',), 'main', ('id', 'main',), False,),
    ('delaney2', None, None, 'main', ('id', 'main',), False,),
    ('gabbard', 'div', ('class', 'main-menus',), 'article', ('class', 's-article',), False,),
    ('gillibrand', 'nav', ('id', 'nav-header',), 'article', None, False,),
    ('gillibrand2', None, None, 'article', None, False,),
    ('harris', 'nav', ('class', 'primary',), 'div', ('class', 'content',), False,),
    ('hickenlooper', 'nav', ('class', 'elementor-nav-menu__container',), 'div', ('class', 'elementor-widget-text-editor',), False,),
    ('inslee', 'nav', ('class', 'primary',), 'article', None, False,),
    ('inslee2', None, None, 'div', ('class', 'main',), False,),
    ('klobuchar', 'ul', ('id', 'menu-main-menu',), 'div', ('class', 'article'), False,),
    ('orourke', 'nav', ('class', 'header__nav',), 'article', None, True,),
    ('ryan', 'nav', None, 'div', ('class', 'wpb_wrapper',), False),
    ('sanders', 'nav', ('id', 'menu-main-header',), 'article', None, False,),
    ('sanders2', None, None, 'article', None, False,),
)

def pickle_candidates():
    for name, nav_tag, nav_attr, c_tag, c_attr, bad in CANDIDATES:
        c = Candidate(name, nav_tag, nav_attr, c_tag, c_attr, bad)
        c.load_links()
        pickle.dump(c.links, open('%s.links' % name, 'wb'))
        c.load_lines()
        line_file =  open('%s.lines' % name, 'wb')
        for line in c.lines:
            line_file.write("%s\n" % line)
        line_file.close()

def test_candidates():
    for name, nav_tag, nav_attr, c_tag, c_attr, bad in CANDIDATES:
        c = Candidate(name, nav_tag, nav_attr, c_tag, c_attr, bad)
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
                    print 'test: %s' % l
            for l in c.lines:
                if l not in test_lines:
                    print 'current: %s' % l
if __name__ == '__main__':
#    pickle_candidates()
    test_candidates()

