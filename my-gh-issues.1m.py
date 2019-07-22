#!/usr/bin/env PYTHONIOENCODING=UTF-8 python
# -*- coding: utf-8 -*-

# <bitbar.title>GitHub Issue Assignments</bitbar.title>
# <bitbar.version>v1.0.0</bitbar.version>
# <bitbar.author>Ross Hendry</bitbar.author>
# <bitbar.author.github>chooban</bitbar.author.github>
# <bitbar.desc>GitHub issue assignments in your menu bar</bitbar.desc>
# <bitbar.image>https://i.imgur.com/hW7dw9E.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>

import json
import urllib2
import os
import sys
import re
from itertools import groupby


# GitHub.com
# github_api_key = os.getenv( 'GITHUB_TOKEN', 'Enter your GitHub.com Personal Access Token here...' )
github_api_key = ''


def get_dict_subset(thedict, *keys):
    return dict([(key, thedict[key]) for key in keys if key in thedict])


def print_bitbar_line(title, **kwargs):
    print title + ' | ' + (' '.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))


def make_github_request(url, method='GET', data=None):
    try:
        headers = {
            'Authorization': 'token ' + github_api_key,
            'Accept': 'application/json',
        }
        if data is not None:
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = len(data)
        request = urllib2.Request(url, headers=headers)
        request.get_method = lambda: method
        response = urllib2.urlopen(request, data)
        return json.load(response) if response.headers.get('content-length', 0) > 0 else {}
    except Exception:
        return None


def get_issues():
    return make_github_request('https://api.github.com/issues')


def format_issue(issue):
    formatted = {
        'title': issue['title'],
        'href': issue['html_url'],
        'image': 'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAQCAYAAAAmlE46AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAA',
    }
    if len(formatted['title']) > 90:
        formatted['title'] = formatted['title'][:79] + '…'

    formatted['title'] = formatted['title'].replace('|', '-')

    return formatted

print 'Github Issues'
print '---'

issues = get_issues()
sorted_issues = sorted(issues, key=lambda issue: issue['repository']['full_name'])
for repo, repo_issues in groupby(sorted_issues, key=lambda issue: issue['repository']['full_name']):
    if repo:
        repo_issues = list(repo_issues)
        print_bitbar_line(title=repo, href=repo_issues[0]['repository_url'] + '/issues/')
        for issue in repo_issues:
            formatted_issue = format_issue(issue)
            print_bitbar_line(title='- ' + formatted_issue['title'], **get_dict_subset(formatted_issue, 'href', 'image'))


