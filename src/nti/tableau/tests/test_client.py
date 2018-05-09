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

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import os
import shutil
import tempfile
import unittest
from six import StringIO

import fudge

from nti.tableau.client import Client
from nti.tableau.client import export_view

from nti.tableau.model import TableauInstance

from nti.tableau.tests import SharedConfiguringTestLayer

from nti.tableau.interfaces import IView
from nti.tableau.interfaces import IWorkbook
from nti.tableau.interfaces import ICredentials


class TestClient(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def tableau(self):
        return TableauInstance(url="https://tableau.ou.edu",
                               site="gjh",
                               username="higg2108",
                               password="mypassword")

    def test_coverage(self):
        client = Client()
        assert_that(client,
                    has_properties('tableau', is_(none())))

    @fudge.patch('requests.get')
    def test_workbooks(self, mock_get):
        client = Client(self.tableau())
        client.credentials = fudge.Fake().has_attr(site_id='cb0f02e9',
                                                   user_id='d1d34a6e',
                                                   token='6kOfTuDK')
        data = u"""
        <?xml version='1.0' encoding='UTF-8'?>
        <tsResponse xmlns="http://tableau.com/api"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://tableau.com/api
                    http://tableau.com/api/ts-api-2.3.xsd">
            <workbooks>
                <workbook id="3c3c4ef3" name="major" contentUrl="major"
                          showTabs="false" size="1" createdAt="2018-01-24T17:16:45Z"
                          updatedAt="2018-02-19T22:25:21Z">
                    <project id="9ba87b35" name="Default"/>
                    <owner id="b163ca04"/>
                    <tags>
                        <tag label="Majors"/>
                    </tags>
                    <views>
                        <view id="9a8a7b6b" contentUrl="Students/Majors" />
                    </views>
                </workbook>
            <workbooks>
        </tsResponse>
        """
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=200)
        mock_get.is_callable().returns(data)
        result = client.get_workbooks()
        assert_that(result, has_length(1))
        assert_that(result[0], validly_provides(IWorkbook))
        assert_that(result[0], verifiably_provides(IWorkbook))
        assert_that(result[0],
                    has_properties('id', '3c3c4ef3',
                                   'name', 'major',
                                   'contentUrl', 'major',
                                   'size', 1,
                                   'owner', 'b163ca04',
                                   'tags', is_(['Majors']),
                                   'createdAt', is_(float),
                                   'updatedAt', is_(float),
                                   'project', has_properties('id', '9ba87b35',
                                                             'name', 'Default')))

        data = u"ERROR"
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=401)
        mock_get.is_callable().returns(data)
        result = client.workbooks()
        assert_that(result, is_(none()))

    @fudge.patch('requests.get')
    def test_query_workbook(self, mock_get):
        client = Client(self.tableau())
        client.credentials = fudge.Fake().has_attr(site_id='cb0f02e9',
                                                   user_id='d1d34a6e',
                                                   token='6kOfTuDK')
        data = u"""
        <?xml version='1.0' encoding='UTF-8'?>
        <tsResponse xmlns="http://tableau.com/api"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://tableau.com/api
                    http://tableau.com/api/ts-api-2.3.xsd">
            <workbook id="3c3c4ef3" name="major" contentUrl="major"
                      showTabs="false" size="1" createdAt="2018-01-24T17:16:45Z"
                      updatedAt="2018-02-19T22:25:21Z">
                <project id="9ba87b35" name="Default"/>
                <owner id="b163ca04"/>
                <tags>
                    <tag label="Majors"/>
                </tags>
                <views>
                    <view id="9a8a7b6b" contentUrl="Students/Majors" />
                </views>
            </workbook>
        </tsResponse>
        """
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=200)
        mock_get.is_callable().returns(data)
        workbook = client.query_workbook('e32c29b7')
        assert_that(workbook, is_not(none()))

        data = u"ERROR"
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=401)
        mock_get.is_callable().returns(data)
        result = client.query_workbook('xddz')
        assert_that(result, is_(none()))

    @fudge.patch('requests.get')
    def test_views(self, mock_get):
        client = Client(self.tableau())
        client.credentials = fudge.Fake().has_attr(site_id='cb0f02e9',
                                                   user_id='d1d34a6e',
                                                   token='6kOfTuDK')
        data = u"""
        <?xml version='1.0' encoding='UTF-8'?>
        <tsResponse>
            <views>
                <view id="view-id" 
                    name="view-name" 
                    contentUrl="content-url" >
                    <workbook id="workbook-id" />
                    <owner id="owner-id" />
                </view>
            </views>
        </tsResponse>
        """
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=200)
        mock_get.is_callable().returns(data)
        result = client.query_views()
        assert_that(result, has_length(1))
        assert_that(result[0], validly_provides(IView))
        assert_that(result[0], verifiably_provides(IView))
        assert_that(result[0],
                    has_properties('id', 'view-id',
                                   'name', 'view-name',
                                   'contentUrl', 'content-url',
                                   'owner', 'owner-id'))

        data = u"ERROR"
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=401)
        mock_get.is_callable().returns(data)
        result = client.query_views()
        assert_that(result, is_(none()))

    @fudge.patch('requests.get')
    def test_search_view(self, mock_get):
        client = Client(self.tableau())
        client.credentials = fudge.Fake().has_attr(site_id='cb0f02e9',
                                                   user_id='d1d34a6e',
                                                   token='6kOfTuDK')
        data = u"""
        <?xml version='1.0' encoding='UTF-8'?>
        <tsResponse>
            <views>
                <view id="myview" 
                    name="view-name" 
                    contentUrl="content-url" >
                    <workbook id="workbook-id" />
                    <owner id="owner-id" />
                </view>
            </views>
        </tsResponse>
        """
        data = fudge.Fake().has_attr(text=data).has_attr(status_code=200)
        mock_get.is_callable().returns(data)
        result = client.search_view("myview")
        assert_that(result, is_not(none()))
        # no hit
        result = client.search_view("xxx")
        assert_that(result, is_(none()))

    @fudge.patch('requests.get')
    def test_export_view(self, mock_get):
        data = StringIO("mydata")
        response = fudge.Fake().has_attr(raw=data).has_attr(status_code=200)
        mock_get.is_callable().returns(response)
        client = Client(self.tableau())
        client.credentials = fudge.Fake().has_attr(site_id='cb0f02e9',
                                                   user_id='d1d34a6e',
                                                   token='6kOfTuDK')
        tempdir = tempfile.mkdtemp()
        try:
            path = os.path.join(tempdir, 'out.csv')
            result = client.export_view('view_id', path)
            assert_that(result, is_(path))
        finally:
            shutil.rmtree(tempdir, True)

        response = fudge.Fake().has_attr(text="ERROR").has_attr(status_code=403)
        mock_get.is_callable().returns(response)
        result = client.export_view('view_id')
        assert_that(result, is_(none()))

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
        assert_that(result, validly_provides(ICredentials))
        assert_that(result, verifiably_provides(ICredentials))
        assert_that(result,
                    has_properties('site_id', 'cb0f02e9',
                                   'user_id', 'd1d34a6e',
                                   'token', '6kOfTuDK'))
        # signout
        client.sign_out()
        assert_that(client,
                    has_properties('credentials', is_(none())))
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

    @fudge.patch('nti.tableau.client.Client.sign_in',
                 'nti.tableau.client.Client.export_view',
                 'nti.tableau.client.Client.sign_out')
    def test_export_view_call(self, mock_sign_in, mock_export_view, mock_sign_out):
        mock_sign_in.expects_call().returns_fake()
        mock_sign_out.expects_call().returns_fake()
        mock_export_view.expects_call().returns_fake()
        export_view('myview', '/tmp', self.tableau())
