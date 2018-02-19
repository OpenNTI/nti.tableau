#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_properties

import unittest

import fudge

from nti.tableau.client import Client

from nti.tableau.model import TableauInstance


class TestClient(unittest.TestCase):

    def tableau(self):
        return TableauInstance(url="https://tableau.ou.edu",
                               site="gjh",
                               username="higg2108",
                               password="N3xtTh0ught!!C")

    def test_coverage(self):
        client = Client()
        assert_that(client,
                    has_properties('tableau', is_(none())))

    @fudge.patch('requests.post')
    def test_sign_in(self, mock_post):
        client = Client(self.tableau())
        data = u"""
        <?xml version='1.0' encoding='UTF-8'?>
        <tsResponse xmlns="http://tableau.com/api"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://tableau.com/api
                    http://tableau.com/api/ts-api-2.3.xsd">
            <credentials token="6kOfTuDK">
                <site id="cb0f02e9" contentUrl="gjh" />
                <user id="d1d34a6e" />
            </credentials>
        </tsResponse>
        """
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=200)
        mock_post.is_callable().returns(data)
        result = client.sign_in()
        assert_that(result, is_not(none()))
        assert_that(result, has_length(3))
        assert_that(client,
                    has_properties('site_id', 'cb0f02e9',
                                   'user_id', 'd1d34a6e',
                                   'token', '6kOfTuDK'))
        # signout
        client.sign_out()
        assert_that(client,
                    has_properties('site_id', is_(none()),
                                   'user_id', is_(none()),
                                   'token', is_(none())))
        # invalid response
        data = u"""
        <?xml version='1.0' encoding='UTF-8'?>
        <tsResponse xmlns="http://tableau.com/api"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://tableau.com/api http://tableau.com/api/ts-api-2.3.xsd">
            <error code="401001">
                <summary>Signin Error</summary>
                <detail>Error signing in to Tableau Server</detail>
            </error>
        </tsResponse>
        """
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=401)
        mock_post.is_callable().returns(data)
        result = client.sign_in()
        assert_that(result, is_(none()))