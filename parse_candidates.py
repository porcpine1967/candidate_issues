#!/usr/bin/env python

import urllib2, HTMLParser

BLOCK_TAGS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'article', 'header', 'section', 'li', 'blockquote', 'nav', 'title', 'footer', 'br', 'main', 'aside', 'iframe',)
INLINE_TAGS = ('span', 'a', 'i', 'b', 'strong', 'figure', 'img', 'ul', 'style', 'polygon', 'g', 'svg', 'path', 'button', 'ol', 'script', 'source', 'picture', 'sup', 'hr', 'em', 'video', 'cite', 'q',)

def file_as_string(html_file):
    contents = ''
    in_head = True
    for l in html_file:
        if in_head and '</head>' in l:
            in_head = False
        if in_head:
            contents += l.replace('\xc3\xa1', '').replace('&quot;', '').replace('&hellip;', '').replace('\xe2\x80\x9c', '').replace('\xe2\x80\x9d', '').replace("'<div", '').replace('</di/v>', '').replace('&hellip;', '').replace('&#039;', '')
        else:
            contents += l.replace("'<div", '').replace('</di/v>', '</div>').replace('&hellip;', '...').replace('&quot;', '').replace('\\"', '').replace('font-weight: 400;', '')
    html_file.close()
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
        if self.tags == [self.tag]:
            self.tags = []
            return
        self.tags.pop()
        if tag in BLOCK_TAGS:
            self.lines.append('')
        elif tag not in INLINE_TAGS:
            if self.bad:
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
        cp = NavigationHTMLParser(file_as_string(open('%s.html' % self.name)), self.navigation_tag, self.navigation_attr, c_links)
        cp.feed(cp.file_as_string)
        self.links = set([l for l in c_links if 'actblue.com' not in l])

    def load_lines(self):
        if not self.content_tag:
            return
        c_lines = []
        cp = ContentHTMLParser(file_as_string(open('%s.html' % self.name)), self.content_tag, self.content_attr, c_lines, self.bad)
        cp.feed(cp.file_as_string)
        lines = [l.strip() for l in c_lines]
        self.lines = [l for l in lines if l]

    def load_pages(self):
        if not self.urls:
            return
        for url in self.urls:
            page = { 'url': url }
            c_links = set()
            html = file_as_string(urllib2.urlopen(url))
            cp = NavigationHTMLParser(html, self.navigation_tag, self.navigation_attr, c_links)
            cp.feed(cp.file_as_string)
            page['links'] = set([l for l in c_links if 'actblue.com' not in l])
            c_lines = []
            cp = ContentHTMLParser(html, self.content_tag, self.content_attr, c_lines, self.bad)
            cp.feed(cp.file_as_string)
            lines = [l.strip() for l in c_lines]
            page['lines'] = [l for l in lines if l]
            self.pages.append(page)
            

        

def test_navigation():
    c = Candidate('warren', 'nav', ('id', 'js-takeover-menu',), 'section', ('class', 'issues-lp__accordion'), True)
    html = file_as_string(open('%s.html' % c.name))
    cp = NavigationHTMLParser(html, c.navigation_tag, c.navigation_attr, c.links)
    cp.feed(cp.file_as_string)
    for link in sorted(list(c.links)):
        if 'actblue.com' not in link:
            print link

def test_content():
    c = Candidate('yang2', None, None, 'div', ('class', 'entry-content',), False,)
    c_lines = []
    html = file_as_string(open('%s.html' % c.name))
    cp = ContentHTMLParser(html, c.content_tag, c.content_attr, c_lines, c.bad)
    cp.feed(cp.file_as_string)
    lines = [l.strip() for l in c_lines]
    for line in [l for l in lines if l]:
        print line
if __name__ == '__main__':
    test_navigation()

    test_content()
