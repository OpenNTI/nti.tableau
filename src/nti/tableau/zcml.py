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

from nti.tableau.interfaces import ITableauInstance

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


def registerTableauInstance(_context, url, username, password):
    """
    Register a tableau instance with the specified context
    """
    factory = functools.partial(TableauInstance,
                                url=url,
                                password=password,
                                username=username)
    utility(_context, provides=ITableauInstance, factory=factory)
