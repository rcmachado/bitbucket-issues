# coding: utf-8
from __future__ import unicode_literals

import re

from lxml import html


class BaseElement(object):
    def __init__(self, content=None, element=None):
        if content:
            parser = html.fromstring(content)
            self.tree = parser.cssselect('#issues-list')[0]
        else:
            parser = element
            self.tree = element


class IssuesList(BaseElement):
    def __getitem__(self, index):
        items = self.tree.cssselect('table.issues-list > tbody > tr')
        return IssueItem(element=items[index])

    def __len__(self):
        text = self.tree.cssselect('header h1 .secondary')[0].text.strip()
        matched = re.match(r'^\(1–\d+\s+of\s+(?P<total>\d+)\)$', text)
        return int(matched.group('total')) if matched else 0


class IssueItem(BaseElement):
    BUG = 'bug'
    MAJOR = 'major'
    CLOSED = 'closed'

    @property
    def id(self):
        matches = re.match(r'^#(?P<id>\d+):', self.title)
        return int(matches.group('id')) if matches else None

    @property
    def title(self):
        return self.tree.cssselect('a.execute')[0].text

    @property
    def type(self):
        el = self.tree.cssselect('a[title^="Filter by type: "]')[0]
        return el.text.strip()

    @property
    def priority(self):
        el = self.tree.cssselect('a[title^="Filter by priority: "]')[0]
        return el.text.strip()

    @property
    def state(self):
        return self.tree.attrib.get('data-state')

    @property
    def votes(self):
        votes = self.tree.cssselect('.votes')[0].text_content().strip()
        return int(votes) if votes else 0
