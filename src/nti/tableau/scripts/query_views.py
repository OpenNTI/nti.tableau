#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import argparse

from zope import component

from nti.tableau.client import Client

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
    args = arg_parser.parse_args(args)

    # logging
    configure_logging(debug=args.verbose)

    # create context
    create_context(args.env_dir)

    tableau = component.queryUtility(ITableauInstance)
    assert tableau is not None, "Must specify an tableau instance"

    # execute
    client = Client(tableau)
    client.sign_in()
    views = client.query_views()
    for view in views or ():
        print("%s,%s" % (view.id, view.name))


def main(args=None):
    process_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
