#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import argparse

from zope import component

from nti.tableau.client import Client

from nti.tableau.interfaces import IExportView
from nti.tableau.interfaces import ITableauInstance

from nti.tableau.scripts import create_context
from nti.tableau.scripts import configure_logging

logger = __import__('logging').getLogger(__name__)


def process_args(args=None):
    arg_parser = argparse.ArgumentParser(description="Export View")
    arg_parser.add_argument('-v', '--verbose', help="Verbose mode",
                            action='store_true', dest='verbose')
    arg_parser.add_argument('-d', '--env_dir', dest='env_dir',
                            help=" Environment root directory")
    arg_parser.add_argument("-o", "--output", dest='output',
                            help="Output file")
    group = arg_parser.add_mutually_exclusive_group()

    group.add_argument('-n', '--name', dest='name',
                       help="Registered view name")

    group.add_argument('-i', '--vid', dest='view_id',
                       help="View id")
    args = arg_parser.parse_args(args)

    # logging
    configure_logging(debug=args.verbose)

    # create context
    create_context(args.env_dir)

    tableau = component.queryUtility(ITableauInstance)
    assert tableau is not None, "Must specify an tableau instance"

    output = os.path.expanduser(args.output) if args.output else None
    assert output and not os.path.isdir(output), \
          "Must specify an output file"

    name = args.name
    view_id = args.view_id
    if name:
        view = component.queryUtility(IExportView, name)
        assert view is not None, "Must specify an tableau export view"
        view_id = view.view_id

    # check url
    assert view_id, "Must specfify a valid view id"

    # execute
    client = Client(tableau)
    client.sign_in()
    client.export_view(view_id, output)


def main(args=None):
    process_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
