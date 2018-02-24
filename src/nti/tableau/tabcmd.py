#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id:
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import subprocess

from zope import component

from zope.cachedescriptors.property import readproperty

from nti.tableau.interfaces import ITableauInstance

logger = __import__('logging').getLogger(__name__)


class PyTabCmd(object):

    no_certcheck = True

    def __init__(self, tableau=None):
        if tableau is not None:
            self.tableau = tableau

    @readproperty
    def tableau(self):  # pylint: disable=method-hidden
        return component.queryUtility(ITableauInstance)

    def _execute_command(self, command):
        command += ["--no-certcheck"] if self.no_certcheck else command
        return subprocess.check_call(command)

    def login(self):
        command = [
            self.tableau.tabcmd,
            'login',
            "-u", "%s" % self.tableau.username,
            "-p", "%s" % self.tableau.password,
            "-s", "%s" % self.tableau.url,
            "-t", "%s" % self.tableau.site,
        ]
        return self._execute_command(command)
