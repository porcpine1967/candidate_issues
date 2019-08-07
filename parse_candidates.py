#!/usr/bin/env python

import HTMLParser
import re
import sys
import urllib2

from candidates import CANDIDATES

BLOCK_TAGS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'article', 'header', 'section', 'li', 'blockquote', 'nav', 'title', 'footer', 'br', 'main', 'aside', 'iframe', 'table', 'tbody', 'tr', 'center', 'figcaption')
INLINE_TAGS = ('span', 'a', 'i', 'b', 'strong', 'figure', 'img', 'ul', 'style', 'polygon', 'g', 'svg', 'path', 'ol', 'script', 'source', 'picture', 'sup', 'hr', 'em', 'video', 'cite', 'q', 'u', 'ins', 'small', 'noscript', 'link', 'td', 'font',)
REPLACEMENTS = ((re.compile(r'<head.*</head>'), '',),
                (re.compile(r'<script.*?</script>'), '',),
                (re.compile(r'<style.*?</style>'), '',),
                (re.compile(r'<form.*?</form>'), '',),
                (re.compile(r'<button.*?</button>'), '',),
                (re.compile(r'<svg.*?</svg>'), '',),
                (re.compile(r'="[^"]*&[^"]*;[^"]*'), '="',),
                ('</di/v>', '</div>',),)
PAGE_LOCATION = re.compile(r'#[^/]*$')

def file_as_string(html_file):
    contents = ''
    for l in html_file:
        contents += l.replace('\n', ' ')
    html_file.close()
    for pattern, replacement in REPLACEMENTS:
        contents = re.sub(pattern, replacement, contents)
    return contents

class ContentHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html, content_tag, content_attr, lines, bad = False):
        HTMLParser.HTMLParser.__init__(self)
        self.tag = content_tag
        self.file_as_string = html
        self.tags = []
        self.lines = lines
        self.bad = bad
        if content_attr:
            self.attr_key, self.attr_value = content_attr
        else:
            self.attr_key = None

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
        if len(self.lines) == 0:
            self.lines.append('')

    def handle_endtag(self, tag):
        if not self.tags:
            return
        if self.tags == [self.tag] or (self.bad == 'nested' and self.tag == tag):
            self.tags = []
            return
        if self.bad != 'unmatched' or tag == self.tags[-1]:
            self.tags.pop()
        if tag in BLOCK_TAGS:
            self.lines.append('')
        elif tag not in INLINE_TAGS:
            if self.bad == 'not nested':
                self.tags = []
            else:
                raise StandardError(tag)

    def handle_data(self, data):
        if self.tags:
            if data.isspace():
                self.lines[-1] += ' '
            else:
                self.lines[-1] += data
                

class NavigationHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, html, host, links):
        HTMLParser.HTMLParser.__init__(self)
        self.host = host
        self.file_as_string = html
        self.tags = []
        self.links = links

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and not value.startswith('#') and value not in ('', '/',):
                    new_value = re.sub(PAGE_LOCATION, '', value)
                    if value.startswith('/'):
                        self.links.add('{}{}'.format(self.host, new_value))
                    elif value.startswith(self.host) or value.startswith('https://medium.com'):
                        self.links.add(new_value)

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
    def __init__(self, name, host, link_bundles):
        self.name = name
        self.host = host
        self.link_bundles = link_bundles
        self.links = set()
        self.lines = []
        self.pages = []

    def load_links(self):
        c_links = set()
        cp = NavigationHTMLParser(file_as_string(open('data/test/%s.html' % self.name)), self.host, c_links)
        cp.feed(cp.file_as_string)
        self.links = set([l for l in c_links if 'actblue.com' not in l and '/cdn-cgi/l/email-protection' not in l])

    def load_lines(self):
        c_lines = []
        content_tag, content_attr, bad, _ = self.link_bundles[0]
        cp = ContentHTMLParser(file_as_string(open('data/test/%s.html' % self.name)), content_tag, content_attr, c_lines, bad)
        cp.feed(cp.file_as_string)
        lines = [l.strip() for l in c_lines]
        self.lines = [l for l in lines if l]

    def load_pages(self):
        print self.name
        if not self.link_bundles:
            return
        for tag, attr, bad, urls in self.link_bundles:
            for url in urls:
                page = { 'url': url }
                page['filename'] = [part for part in url.split('/') if part][-1]
                print ' ', page['filename']
                req = urllib2.Request(url)
                req.add_header('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
                html = file_as_string(urllib2.urlopen(req))
                if url.startswith(self.host):
                    c_links = set()
                    cp = NavigationHTMLParser(html, self.host, c_links)
                    cp.feed(cp.file_as_string)
                    self.links.update(set([l for l in c_links if 'actblue.com' not in l and '/cdn-cgi/l/email-protection' not in l]))
                c_lines = []
                cp = ContentHTMLParser(html, tag, attr, c_lines, bad)
                cp.feed(cp.file_as_string)
                lines = [l.strip() for l in c_lines]
                page['lines'] = [l for l in lines if l]
                self.pages.append(page)
            

        

def test_navigation():
    if len(sys.argv) > 1:
        found = False
        for name, host, link_bundles in CANDIDATES:
            if name == sys.argv[1]:
                c = Candidate(name, host, link_bundles)
                found = True
                break
        if not found:
            print 'No such candidate', sys.argv[1]
            sys.exit(1)
    else:
        print 'Please pick a candidate'
        sys.exit(1)
    html = file_as_string(open('data/test/%s.html' % c.name))
    cp = NavigationHTMLParser(html, c.host, c.links)
    cp.feed(cp.file_as_string)
    for link in sorted(list(c.links)):
        if 'actblue.com' not in link:
            print link

def test_content():
    if len(sys.argv) > 1:
        found = False
        for name, host, link_bundles in CANDIDATES:
            if name == sys.argv[1]:
                c = Candidate(name, host, link_bundles)
                found = True
                break
        if not found:
            print 'No such candidate', sys.argv[1]
            sys.exit(1)
    else:
        print 'Please pick a candidate'
        sys.exit(1)
    c_lines = []
    html = file_as_string(open('data/test/%s.html' % c.name))
    content_tag, content_attr, bad, _ = c.link_bundles[0]
    cp = ContentHTMLParser(html, content_tag, content_attr, c_lines, bad)
    cp.feed(cp.file_as_string)
    lines = [l.strip() for l in c_lines]
    for line in [l for l in lines if l]:
        print line
if __name__ == '__main__':
#    test_navigation()

    test_content()
