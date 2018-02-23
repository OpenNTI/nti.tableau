#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_properties

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from zope import component

from nti.tableau import API_VERSION

from nti.tableau.interfaces import IExportView
from nti.tableau.interfaces import ITableauInstance 

import nti.testing.base

ZCML_STRING = u"""
<configure xmlns="http://namespaces.zope.org/zope"
    xmlns:zcml="http://namespaces.zope.org/zcml"
    xmlns:tableau="http://nextthought.com/ntp/tableau"
    i18n_domain='nti.tableau'>

    <include package="zope.component" />

    <include package="." file="meta.zcml" />

    <tableau:registerTableauInstance
                    url="https://tableau.nextthought.com" 
                    username="myuser" 
                    password="mypassword"
                    site="mysite" />
                    
    <tableau:registerExportView
                    name="persons" 
                    contentURL="person/Person" />
</configure>
"""


class TestZcml(nti.testing.base.ConfiguringTestBase):

    def test_registrations(self):
        self.configure_string(ZCML_STRING)
        # tableau
        tableau = component.queryUtility(ITableauInstance)
        assert_that(tableau, is_not(none()))
        assert_that(tableau, validly_provides(ITableauInstance))
        assert_that(tableau, verifiably_provides(ITableauInstance))
        assert_that(tableau,
                    has_properties("url", "https://tableau.nextthought.com",
                                   "site", "mysite",
                                   "username", "myuser",
                                   "password", "mypassword",
                                   "api_version", API_VERSION))
        # view
        view = component.queryUtility(IExportView, name="persons")
        assert_that(view, is_not(none()))
        assert_that(view, validly_provides(IExportView))
        assert_that(view, verifiably_provides(IExportView))
        assert_that(view,
                    has_properties("name", "persons",
                                   "contentUrl", "person/Person"))
