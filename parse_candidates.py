#!/usr/bin/env python

import re,  datetime, HTMLParser

BLOCK_TAGS = ['h2', 'h3', 'p', 'div', 'article',]
INLINE_TAGS = ['span', 'a', 'i', 'b', 'strong',]

class ContentHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html_file, candidate):
        HTMLParser.HTMLParser.__init__(self)
        self.tag = candidate.content_tag
        self.file_as_string = ""
        for l in html_file:
            self.file_as_string += l
        self.tags = []
        self.lines = []

    def handle_starttag(self, tag, attrs):
        if len(self.tags) or tag == self.tag:
            self.tags.append(tag)
            if tag in BLOCK_TAGS:
                self.lines.append('')
            elif tag not in INLINE_TAGS:
                raise StandardError(tag)

    def handle_endtag(self, tag):
        if not self.tags:
            return
        if self.tags == [self.tag]:
            self.tags = []
            return
        self.tags.pop()

    def handle_data(self, data):
        if self.tags:
            self.lines[-1] += data
                

class NavigationHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html_file, candidate):
        HTMLParser.HTMLParser.__init__(self)
        self.tag = candidate.navigation_tag
        self.file_as_string = ""
        for l in html_file:
            self.file_as_string += l
        self.tags = []
        self.links = set()

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

def test_navigation():
    c = Candidate('bennet', 'nav', '')
    cp = NavigationHTMLParser(open('bennet.html'), c)
    cp.feed(cp.file_as_string)
    for link in sorted(list(cp.links)):
        print link

def test_content():
    c = Candidate('bennet', 'nav', 'article')
    cp = ContentHTMLParser(open('bennet.html'), c)
    cp.feed(cp.file_as_string)
    lines = [l.strip() for l in cp.lines]
    for line in [l for l in lines if l]:
        print line
if __name__ == '__main__':
    test_content()
