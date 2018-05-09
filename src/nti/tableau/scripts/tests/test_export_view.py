#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,no-member

import os
import unittest

import fudge

from nti.tableau.scripts.export_view import process_args
from nti.tableau.scripts.export_view import main as sync_main


class TestExportView(unittest.TestCase):

    @fudge.patch('nti.tableau.scripts.export_view.process_args')
    def test_main(self, mock_pa):
        mock_pa.expects_call().returns_fake()
        sync_main()

    @fudge.patch('nti.tableau.scripts.export_view.export_view',)
    def test_process_args(self, mock_export_view):
        mock_export_view.expects_call().returns_fake()
        dirname = os.path.dirname(__file__)
        output = os.path.join(dirname, "output.csv")
        params = "-d %s -n persons -o %s" % (dirname, output)
        process_args(params.split())
