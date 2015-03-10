# coding: utf-8
from __future__ import unicode_literals

import codecs
import os

import pytest

from ..parser import IssuesList, IssueItem


@pytest.fixture
def issues_content():
    filename = os.path.join(os.path.dirname(__file__),
                            'fixtures', 'issues-list.html')
    fd = codecs.open(filename, 'r', encoding='utf-8')
    content = fd.read()
    fd.close()
    return content


def test_return_total_issues(issues_content):
    issues = IssuesList(issues_content)
    assert 799 == len(issues)


def test_get_issue_item(issues_content):
    issues = IssuesList(issues_content)
    assert isinstance(issues[0], IssueItem) is True


def test_get_issue_title(issues_content):
    title = ('#1088: Some Python exception classes not highlighted '
             '(e.g. BlockingIOError)')
    issues = IssuesList(issues_content)
    assert title == issues[0].title


def test_get_issue_id(issues_content):
    issues = IssuesList(issues_content)
    assert 1088 == issues[0].id


def test_get_issue_type(issues_content):
    issues = IssuesList(issues_content)
    assert IssueItem.BUG == issues[0].type


def test_get_issue_priority(issues_content):
    issues = IssuesList(issues_content)
    assert IssueItem.MAJOR == issues[0].priority


def test_get_issue_state(issues_content):
    issues = IssuesList(issues_content)
    assert IssueItem.CLOSED == issues[0].state


def test_get_issue_votes(issues_content):
    issues = IssuesList(issues_content)
    assert 0 == issues[0].votes
    assert 1 == issues[1].votes
