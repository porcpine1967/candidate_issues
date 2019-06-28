#!/usr/bin/env python

import HTMLParser
import re
import sys
import urllib2

from candidates import CANDIDATES

BLOCK_TAGS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'article', 'header', 'section', 'li', 'blockquote', 'nav', 'title', 'footer', 'br', 'main', 'aside', 'iframe',)
INLINE_TAGS = ('span', 'a', 'i', 'b', 'strong', 'figure', 'img', 'ul', 'style', 'polygon', 'g', 'svg', 'path', 'ol', 'script', 'source', 'picture', 'sup', 'hr', 'em', 'video', 'cite', 'q', 'u', 'ins', 'small', 'noscript', 'link',)
IGNORE_TAGS = ('form', 'script', 'style', 'button', 'svg',)

def file_as_string(html_file):
    contents = ''
    t = ''
    in_head = True
    for l in html_file:
        t += l
        if in_head and '</head>' in l:
            in_head = False
        if in_head:
            contents += l.replace('\xc3\xa1', '').replace('&quot;', '').replace('&hellip;', '').replace('\xe2\x80\x9c', '').replace('\xe2\x80\x9d', '').replace("'<div", '').replace('</di/v>', '').replace('&hellip;', '').replace('&#039;', '').replace('&#8217;', '').replace('&nbsp;', '')
        else:
            contents += l.replace("'<div", '').replace('</di/v>', '</div>').replace('&hellip;', '...').replace('&quot;', '').replace('\\"', '').replace('font-weight: 400;', '').replace("\n", ' ')
    html_file.close()
    return re.sub(r'data-main="[^"]+"', '', contents)

class ContentHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html, content_tag, content_attr, lines, bad = False):
        HTMLParser.HTMLParser.__init__(self)
        self.tag = content_tag
        self.file_as_string = html
        self.tags = []
        self.lines = lines
        self.bad = bad
        self.ignore_tag = None
        if content_attr:
            self.attr_key, self.attr_value = content_attr
        else:
            self.attr_key = None

    def handle_starttag(self, tag, attrs):
        if tag in IGNORE_TAGS and not self.ignore_tag:
            self.ignore_tag = tag
        if self.attr_key and tag == self.tag and not self.tags:
            found = False
            for key, value in attrs:
                if key == self.attr_key:
                    for subvalue in value.split():
                        if subvalue == self.attr_value:
                            found = True
            if not found:
                return
        if len(self.tags) or tag == self.tag:
            self.tags.append(tag)
        if len(self.lines) == 0:
            self.lines.append('')

    def handle_endtag(self, tag):
        if tag == self.ignore_tag:
            self.ignore_tag = None
        if not self.tags:
            return
        if self.tags == [self.tag] or (self.bad > 0 and self.tag == tag):
            self.tags = []
            return
        self.tags.pop()
        if tag in BLOCK_TAGS:
            self.lines.append('')
        elif tag not in INLINE_TAGS and tag not in IGNORE_TAGS:
            if self.bad < 0:
                self.tags = []
            elif not self.ignore_tag:
                raise StandardError(tag)

    def handle_data(self, data):
        if self.tags and not self.ignore_tag:
            if data.isspace():
                self.lines[-1] += ' '
            else:
                self.lines[-1] += data
                

class NavigationHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html, navigation_tag, navigation_attr, links):
        HTMLParser.HTMLParser.__init__(self)
        self.tag = navigation_tag
        if navigation_attr:
            self.attr_key, self.attr_value = navigation_attr
        else:
            self.attr_key = None
        self.file_as_string = html
        self.tags = []
        self.links = links

    def handle_starttag(self, tag, attrs):
        if self.attr_key and tag == self.tag and not self.tags:
            found = False
            for key, value in attrs:
                if key == self.attr_key:
                    for subvalue in value.split():
                        if subvalue == self.attr_value:
                            found = True
            if not found:
                return
        if len(self.tags) or tag == self.tag:
            self.tags.append(tag)
            if tag == 'a':
                for attr, value in attrs:
                    if attr == 'href' and not value.startswith('#') and value not in ('', '/',):
                        self.links.add(value)

    def handle_endtag(self, tag):
        if not self.tags:
            return
        if self.tags == [self.tag]:
            self.tags = []
            return
        self.tags.pop()
        

    def handle_data(self, data):
        pass

class Candidate(object):
    def __init__(self, name, navigation_tag, navigation_attr, content_tag, content_attr, bad=False, urls=None):
        self.name = name
        self.navigation_tag = navigation_tag
        self.navigation_attr = navigation_attr
        self.content_tag = content_tag
        self.content_attr = content_attr
        self.links = set()
        self.lines = []
        self.bad = bad
        self.urls = urls
        self.pages = []

    def load_links(self):
        c_links = set()
        cp = NavigationHTMLParser(file_as_string(open('data/test/%s.html' % self.name)), self.navigation_tag, self.navigation_attr, c_links)
        cp.feed(cp.file_as_string)
        self.links = set([l for l in c_links if 'actblue.com' not in l and '/cdn-cgi/l/email-protection' not in l])

    def load_lines(self):
        if not self.content_tag:
            return
        c_lines = []
        cp = ContentHTMLParser(file_as_string(open('data/test/%s.html' % self.name)), self.content_tag, self.content_attr, c_lines, self.bad)
        cp.feed(cp.file_as_string)
        lines = [l.strip() for l in c_lines]
        self.lines = [l for l in lines if l]

    def load_pages(self):
        print self.name
        if not self.urls:
            return
        for url in self.urls:
            page = { 'url': url }
            page['filename'] = [part for part in url.split('/') if part][-1]
            print page['filename']
            req = urllib2.Request(url)
            req.add_header('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
            html = file_as_string(urllib2.urlopen(req))
            c_links = set()
            cp = NavigationHTMLParser(html, self.navigation_tag, self.navigation_attr, c_links)
            cp.feed(cp.file_as_string)
            self.links.update(set([l for l in c_links if 'actblue.com' not in l and '/cdn-cgi/l/email-protection' not in l]))
            c_lines = []
            cp = ContentHTMLParser(html, self.content_tag, self.content_attr, c_lines, self.bad)
            cp.feed(cp.file_as_string)
            lines = [l.strip() for l in c_lines]
            page['lines'] = [l for l in lines if l]
            self.pages.append(page)
            

        

def test_navigation():
    if len(sys.argv) > 1:
        found = False
        for name, nav_tag, nav_attr, c_tag, c_attr, bad, _ in CANDIDATES:
            if name == sys.argv[1]:
                c = Candidate(name, nav_tag, nav_attr, c_tag, c_attr, bad)
                found = True
        if not found:
            print 'No such candidate', sys.argv[1]
            sys.exit(1)
    else:
        c = Candidate('gabbard', 'nav', ('id', 'js-takeover-menu',), 'section', ('class', 'issues-lp__accordion'), True)
    html = file_as_string(open('data/test/%s.html' % c.name))
    cp = NavigationHTMLParser(html, c.navigation_tag, c.navigation_attr, c.links)
    cp.feed(cp.file_as_string)
    for link in sorted(list(c.links)):
        if 'actblue.com' not in link:
            print link

def test_content():
    if len(sys.argv) > 1:
        found = False
        for name, nav_tag, nav_attr, c_tag, c_attr, bad, _ in CANDIDATES:
            if name == sys.argv[1]:
                c = Candidate(name, nav_tag, nav_attr, c_tag, c_attr, bad)
                found = True
        if not found:
            print 'No such candidate', sys.argv[1]
            sys.exit(1)
    else:
        c = Candidate('gabbard', 'nav', ('id', 'js-takeover-menu',), 'section', ('class', 'issues-lp__accordion'), True)
    c_lines = []
    html = file_as_string(open('data/test/%s.html' % c.name))
    cp = ContentHTMLParser(html, c.content_tag, c.content_attr, c_lines, c.bad)
    cp.feed(cp.file_as_string)
    lines = [l.strip() for l in c_lines]
    for line in [l for l in lines if l]:
        print line
if __name__ == '__main__':
    test_navigation()

    test_content()
