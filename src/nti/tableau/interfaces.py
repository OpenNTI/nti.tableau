#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface

from nti.schema.field import ValidURI
from nti.schema.field import DecodingValidTextLine as TextLine

from nti.tableau import API_VERSION


class ITableauInstance(interface.Interface):
    """
    Defines a Tableau instance
    """
    url = ValidURI(title=u"The URL", required=True)

    username = TextLine(title=u"The username", required=True)

    password = TextLine(title=u"The password", required=True)

    site = TextLine(title=u"The site",
                    default=u'',
                    required=False)

    api_version = TextLine(title=u"The api version",
                           default=API_VERSION,
                           required=True)
