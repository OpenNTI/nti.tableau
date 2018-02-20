#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.eqhash import EqHash

from nti.schema.schema import SchemaConfigured

from nti.tableau.interfaces import ISite
from nti.tableau.interfaces import IView
from nti.tableau.interfaces import IProject
from nti.tableau.interfaces import IWorkbook
from nti.tableau.interfaces import ICredentials
from nti.tableau.interfaces import ITableauInstance

logger = __import__('logging').getLogger(__name__)


@interface.implementer(ITableauInstance)
class TableauInstance(SchemaConfigured):
    createDirectFieldProperties(ITableauInstance)


@EqHash('id',)
@interface.implementer(ISite)
class Site(SchemaConfigured):
    createDirectFieldProperties(ISite)


@interface.implementer(ICredentials)
class Credentials(SchemaConfigured):
    createDirectFieldProperties(ICredentials)

    @property
    def site_id(self):
        # pylint: disable=no-member
        return self.site.id if self.site else None


@EqHash('id',)
@interface.implementer(IView)
class View(SchemaConfigured):
    createDirectFieldProperties(IView)


@EqHash('id',)
@interface.implementer(IProject)
class Project(SchemaConfigured):
    createDirectFieldProperties(IProject)


@EqHash('id',)
@interface.implementer(IWorkbook)
class Workbook(SchemaConfigured):
    createDirectFieldProperties(IWorkbook)
