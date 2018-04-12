#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import time

from bs4 import BeautifulSoup

from zope.interface.common.idatetime import IDateTime

from nti.tableau.model import Site
from nti.tableau.model import View
from nti.tableau.model import Project
from nti.tableau.model import Workbook
from nti.tableau.model import Credentials

logger = __import__('logging').getLogger(__name__)


def parse_datetime(value):
    value = IDateTime(value, None) if value else None
    return time.mktime(value.timetuple()) if value is not None else None


def parse_credentials(text):
    """
    Returns the credentials from the specified text
    """
    result = None
    xml_response = BeautifulSoup(text, 'xml')
    node = xml_response.find('credentials')
    if node:
        result = Credentials(token=node.get('token'))
        # site
        site = node.find('site')
        if site:
            site = Site(id=site.get('id'),
                        name=site.get('name'),
                        contentUrl=site.get('contentUrl'))
            result.site = site
        # user
        user = node.find('user')
        if user:
            result.user_id = user.get('id')
    return result


def parse_views(text):
    """
    Returns a list of views from the specified text
    """
    result = []
    xml_response = BeautifulSoup(text, 'xml')
    for node in xml_response.find_all("view"):
        view = View(id=node.get('id'),
                    name=node.get('name'),
                    contentUrl=node.get('contentUrl'))
        # dates
        view.createdAt = parse_datetime(node.get('createdAt'))
        view.updatedAt = parse_datetime(node.get('updatedAt'))
        # workbook
        workbook = node.find('workbook')
        if workbook:
            view.workbook = workbook.get('id')
        # owner
        owner = node.find('owner')
        if owner:
            view.owner = owner.get('id')
        # tags
        tags = set()
        for tag in node.find_all('tag'):
            tags.add(tag.get('label') or None)
        tags.discard(None)
        view.tags = list(tags) if tags else ()
        # add
        result.append(view)
    return result


def parse_workbooks(text):
    """
    Returns a list of workbooks from the specified text
    """
    result = []
    xml_response = BeautifulSoup(text, 'xml')
    for node in xml_response.find_all("workbook"):
        work = Workbook(id=node.get('id'),
                        name=node.get('name'),
                        size=int(node.get('size') or '0'),
                        contentUrl=node.get('contentUrl'))
        # dates
        work.createdAt = parse_datetime(node.get('createdAt'))
        work.updatedAt = parse_datetime(node.get('updatedAt'))
        # project
        project = node.find('project')
        if project:
            project = Project(id=project.get('id'),
                              name=project.get('name'))
            work.project = project
        # owner
        owner = node.find('owner')
        if owner:
            work.owner = owner.get('id')
        # tags
        tags = set()
        for tag in node.find_all('tag'):
            tags.add(tag.get('label') or None)
        tags.discard(None)
        work.tags = list(tags) if tags else ()
        # views
        views = list()
        for view in node.find_all('view'):
            views.append(View(id=view.get('id'),
                              name=view.get('name'),
                              contentUrl=view.get('contentUrl')))
        work.views = views or ()
        # add
        result.append(work)
    return result
