#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,no-member

from hamcrest import raises
from hamcrest import calling
from hamcrest import assert_that

import unittest

from nti.tableau.scripts import create_context
from nti.tableau.scripts import configure_logging


class TestScripts(unittest.TestCase):

    def test_invalid_dir(self):
        assert_that(calling(create_context).with_args('/tmp/__not_valid_dir__'),
                    raises(ValueError))

    def test_configure_logging(self):
        configure_logging()
