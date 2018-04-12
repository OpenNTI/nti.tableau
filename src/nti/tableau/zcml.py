#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id:
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

import functools

from zope import interface

from zope.component.zcml import utility

from zope.configuration import fields

from zope.schema import URI

from nti.tableau import API_VERSION

from nti.tableau.interfaces import IExportView
from nti.tableau.interfaces import ITableauInstance

from nti.tableau.model import ExportView
from nti.tableau.model import TableauInstance

logger = __import__('logging').getLogger(__name__)


class IRegisterTableauInstance(interface.Interface):
    """
    Provides a schema for registering a tableau instance
    """
    url = URI(title=u"Tableau URL", required=True)

    username = fields.TextLine(title=u"The username",
                               required=True)

    password = fields.TextLine(title=u"The password",
                               required=True)

    site = fields.TextLine(title=u"The site",
                           default=u'',
                           required=False)

    api_version = fields.TextLine(title=u"The site",
                                  default=API_VERSION,
                                  required=False)

    tabcmd = fields.TextLine(title=u"The tabcmd location",
                             default=u'tabcmd',
                             required=True)


def registerTableauInstance(_context, url, username, password, site=u'',
                            api_version=API_VERSION, tabcmd=u'tabcmd'):
    """
    Register a tableau instance with the specified context
    """
    factory = functools.partial(TableauInstance,
                                url=url,
                                site=site or u'',
                                password=password,
                                username=username,
                                api_version=api_version,
                                tabcmd=tabcmd or u'tabcmd')
    utility(_context, provides=ITableauInstance, factory=factory)


class IRegisterExportView(interface.Interface):
    """
    Provides a schema for registering a tableau export view
    """
    name = fields.TextLine(title=u"view name", required=True)

    view_id = fields.TextLine(title=u"The view id",
                              required=True)


def registerExportView(_context, name, view_id):
    """
    Register a tableau export view with the specified context
    """
    factory = functools.partial(ExportView,
                                name=name,
                                view_id=view_id)
    utility(_context, provides=IExportView, factory=factory, name=name)
