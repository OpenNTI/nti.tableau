#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import xml.etree.ElementTree as ET

import requests

from zope import component

from zope.cachedescriptors.property import readproperty

from nti.tableau.interfaces import ITableauInstance

from nti.tableau.parsing import parse_workbooks
from nti.tableau.parsing import parse_credentials

logger = __import__('logging').getLogger(__name__)


class Client(object):

    credentials = None

    def __init__(self, tableau=None):
        if tableau is not None:
            self.tableau = tableau

    @readproperty
    def tableau(self):  # pylint: disable=method-hidden
        return component.queryUtility(ITableauInstance)

    @classmethod
    def encode(cls, text):
        return text.encode(
            'ascii', errors="backslashreplace"
        ).decode('utf-8')

    # workbooks

    def get_workbooks(self):
        """
        Returns a list of workbooks that the current user has permission to read
        """
        result = None
        if self.credentials:
            tableau = self.tableau
            # pylint: disable=no-member
            url = "%s/api/%s/sites/%s/users/%s/workbooks" % (tableau.url, tableau.api_version,
                                                             self.credentials.site_id,
                                                             self.credentials.user_id)
            response = requests.get(url,
                                    headers={"x-tableau-auth": self.credentials.token})
            if response.status_code == 200:
                text = self.encode(response.text)
                result = parse_workbooks(text)
            else:
                logger.error("Error getting workbooks [%s]. %s", url,
                             response.text)
        return result
    workbooks = get_workbooks

    def query_workbook(self, workbook):
        """
        Query a workbook
        """
        result = None
        if self.credentials:
            tableau = self.tableau
            wid = getattr(workbook, 'id', workbook)
            # pylint: disable=no-member
            url = "%s/api/%s/sites/%s/workbooks/%s" % (tableau.url, tableau.api_version,
                                                       self.credentials.site_id, wid)
            response = requests.get(url,
                                    headers={"x-tableau-auth": self.credentials.token})
            if response.status_code == 200:
                text = self.encode(response.text)
                result = parse_workbooks(text)
                result = result[0] if result else None
            else:
                logger.error("Error getting workbook [%s]. %s", url,
                             response.text)
        return result

    # login/logout

    def sign_in(self, site=""):
        """
        Signs in to the server

        :param site: Database name is the ID (as a string) of the site on the server 
                     to sign in to. The default is "", which signs in to the default site.

        :type site: str

        :returns: The authentication token, the site ID and the user id
        """
        tableau = self.tableau
        site = site or tableau.site
        url = "%s/api/%s/auth/signin" % (tableau.url, tableau.api_version)

        # Builds the request
        xml_payload_for_request = ET.Element('tsRequest')
        credentials_element = ET.SubElement(xml_payload_for_request,
                                            'credentials',
                                            name=tableau.username,
                                            password=tableau.password)
        ET.SubElement(credentials_element, 'site', contentUrl=site)
        xml_payload_for_request = ET.tostring(xml_payload_for_request)

        # Makes the request to Tableau Server
        response = requests.post(url, data=xml_payload_for_request)
        if response.status_code == 200:
            # Reads and parses the response
            text = self.encode(response.text)
            result = self.credentials = parse_credentials(text)
        else:
            result = None
            logger.error("Cannot sign_in to [%s]. %s", url,
                         response.text)
        return result

    def sign_out(self):
        """
        Destroys the active session
        """
        if self.credentials:
            tableau = self.tableau
            # pylint: disable=no-member
            url = "%s/api/%s/auth/signout" % (tableau.url, tableau.api_version)
            requests.post(url,
                          headers={'x-tableau-auth': self.credentials.token})
            self.credentials = None
