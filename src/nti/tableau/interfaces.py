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

from nti.schema.field import Int
from nti.schema.field import Object
from nti.schema.field import Number
from nti.schema.field import ValidURI
from nti.schema.field import IndexedIterable
from nti.schema.field import DecodingValidTextLine as TextLine

from nti.tableau import API_VERSION


class ICreatedTime(interface.Interface):
    """
    Something that (immutably) tracks its created time.
    """

    createdTime = Number(title=u"The timestamp at which this object was created.",
                         description=u"Typically set automatically by the object.",
                         default=0.0)


class ILastModified(ICreatedTime):
    """
    Something that tracks a modification timestamp.
    """

    lastModified = Number(title=u"The timestamp at which this object or its contents was last modified.",
                          default=0.0)


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

    tabcmd = TextLine(title=u"The tabcmd location",
                      default=u'tabcmd',
                      required=True)


class ISite(interface.Interface):
    """
    Defines a Tableau site
    """
    id = TextLine(title=u"The id", required=True)

    name = TextLine(title=u"The name", required=False)

    contentUrl = TextLine(title=u"The content URL",
                          required=False)


class ICredentials(interface.Interface):
    """
    Defines a Tableau sign-in credentials
    """
    token = TextLine(title=u"The token", required=True)

    user_id = TextLine(title=u"The user id", required=True)

    site = Object(ISite, title=u"The site",
                  required=True)
    site_id = interface.Attribute("The site id")


class IView(ILastModified):
    """
    Defines a Tableau view
    """
    id = TextLine(title=u"The id", required=True)

    name = TextLine(title=u"The name", required=False)

    contentUrl = TextLine(title=u"The content URL",
                          required=False)

    owner = TextLine(title=u"The owner id",
                     required=False)

    workbook = TextLine(title=u"The workbook id",
                        required=False)

    tags = IndexedIterable(title=u"The tags",
                           min_length=0,
                           required=False,
                           value_type=TextLine(title=u"The tag"))


class IExportView(interface.Interface):
    """
    Defines a Tableau export view
    """
    name = TextLine(title=u"The name", required=True)

    view_id = TextLine(title=u"The view id",
                       required=True)


class IProject(interface.Interface):
    """
    Defines a Tableau project
    """
    id = TextLine(title=u"The id", required=True)

    name = TextLine(title=u"The name", required=False)


class IWorkbook(ILastModified):
    """
    Defines a Tableau workbook
    """
    id = TextLine(title=u"The id", required=True)

    name = TextLine(title=u"The name", required=False)

    size = Int(title=u"The size", required=False, default=0)

    contentUrl = TextLine(title=u"The content url",
                          required=False)

    project = Object(IProject, title=u"The project",
                     required=False)

    owner = TextLine(title=u"The owner id",
                     required=False)

    tags = IndexedIterable(title=u"The tags",
                           min_length=0,
                           required=False,
                           value_type=TextLine(title=u"The tag"))

    views = IndexedIterable(title=u"The views",
                            min_length=0,
                            required=False,
                            value_type=Object(IView, title=u"The view"))
