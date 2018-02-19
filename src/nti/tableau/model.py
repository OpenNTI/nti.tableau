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

from nti.schema.schema import SchemaConfigured

from nti.tableau.interfaces import IProject
from nti.tableau.interfaces import IWorkbook
from nti.tableau.interfaces import ITableauInstance

logger = __import__('logging').getLogger(__name__)


@interface.implementer(ITableauInstance)
class TableauInstance(SchemaConfigured):
    createDirectFieldProperties(ITableauInstance)


@interface.implementer(IProject)
class Project(SchemaConfigured):
    createDirectFieldProperties(IProject)


@interface.implementer(IWorkbook)
class Workbook(SchemaConfigured):
    createDirectFieldProperties(IWorkbook)
