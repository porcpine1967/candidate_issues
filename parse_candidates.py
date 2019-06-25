#!/usr/bin/env python

import re,  datetime, HTMLParser

BLOCK_TAGS = ['h1', 'h2', 'h3', 'p', 'div', 'article', 'header', 'section', 'li', 'blockquote']
INLINE_TAGS = ['span', 'a', 'i', 'b', 'strong', 'figure', 'img', 'ul']

class ContentHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html_file, content_tag, lines):
        HTMLParser.HTMLParser.__init__(self)
        self.tag = content_tag
        self.file_as_string = ""
        for l in html_file:
            self.file_as_string += l
        self.tags = []
        self.lines = lines

    def handle_starttag(self, tag, attrs):
        if len(self.tags) or tag == self.tag:
            self.tags.append(tag)
            self.lines.append('')
    def handle_endtag(self, tag):
        if not self.tags:
            return
        if self.tags == [self.tag]:
            self.tags = []
            return
        self.tags.pop()
        if tag in BLOCK_TAGS:
            self.lines.append('')
        elif tag not in INLINE_TAGS:
            raise StandardError(tag)

    def handle_data(self, data):
        if self.tags:
            self.lines[-1] += data
                

class NavigationHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html_file, navigation_tag, links):
        HTMLParser.HTMLParser.__init__(self)
        self.tag = navigation_tag
        self.file_as_string = ""
        for l in html_file:
            self.file_as_string += l
        self.tags = []
        self.links = links

    def handle_starttag(self, tag, attrs):
        if len(self.tags) or tag == self.tag:
            self.tags.append(tag)
            if tag == 'a':
                for attr, value in attrs:
                    if attr == 'href':
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
    def __init__(self, name, navigation_tag, content_tag):
        self.name = name
        self.navigation_tag = navigation_tag
        self.content_tag = content_tag
        self.links = set()
        self.lines = set()

def test_navigation():
    c = Candidate('biden', 'nav', '')
    cp = NavigationHTMLParser(open('biden.html'), c.navigation_tag, c.links)
    cp.feed(cp.file_as_string)
    for link in sorted(list(c.links)):
        print link

def test_content():
    c = Candidate('biden', 'nav', 'article')
    c_lines = []
    cp = ContentHTMLParser(open('biden.html'), c.content_tag, c_lines)
    cp.feed(cp.file_as_string)
    lines = [l.strip() for l in c_lines]
    for line in [l for l in lines if l]:
        print line
if __name__ == '__main__':
#    test_navigation()
    test_content()
