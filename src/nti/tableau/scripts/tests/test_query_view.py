#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,no-member

import os
import unittest

import fudge

from nti.tableau.scripts.query_views import process_args
from nti.tableau.scripts.query_views import main as sync_main


class TestQueryViews(unittest.TestCase):

    @fudge.patch('nti.tableau.scripts.query_views.process_args')
    def test_main(self, mock_pa):
        mock_pa.expects_call().returns_fake()
        sync_main()

    @fudge.patch('nti.tableau.scripts.query_views.Client.sign_in',
                 'nti.tableau.scripts.query_views.Client.query_views')
    def test_process_args(self, mock_sign_in, mock_query):
        mock_sign_in.expects_call().returns_fake()
        view = fudge.Fake().has_attr(id='vid').has_attr(name='vname')
        mock_query.expects_call().returns((view,))
        dirname = os.path.dirname(__file__)
        params = "-d %s" % (dirname,)
        process_args(params.split())
