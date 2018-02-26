#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import assert_that
from hamcrest import has_properties

import unittest

import fudge

from nti.tableau.tabcmd import PyTabCmd

from nti.tableau.model import TableauInstance

from nti.tableau.tests import SharedConfiguringTestLayer


class TestTabCmd(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def tableau(self):
        return TableauInstance(url="https://tableau.ou.edu",
                               site="gjh",
                               username="myuser",
                               password="mypassword")

    def test_coverage(self):
        tabcmd = PyTabCmd()
        assert_that(tabcmd,
                    has_properties('tableau', is_(none())))

    @fudge.patch('subprocess.check_call')
    def test_login(self, mock_call):
        mock_call.is_callable().returns_fake()
        tabcmd = PyTabCmd(self.tableau())
        tabcmd.login()
        
    @fudge.patch('subprocess.check_call')
    def test_export(self, mock_call):
        mock_call.is_callable().returns_fake()
        tabcmd = PyTabCmd(self.tableau())
        tabcmd.export("person/Persons", "-f persons.csv")
