#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

import requests

from zope import component

from zope.cachedescriptors.property import readproperty

from nti.tableau.interfaces import ITableauInstance

XML_NS = {'t': 'http://tableau.com/api'}


logger = __import__('logging').getLogger(__name__)


class Client(object):

    site_id = token = user_id = None

    def __init__(self, tableau=None):
        if tableau is not None:
            self.tableau = tableau

    @readproperty
    def tableau(self):  # pylint: disable=method-hidden
        return component.queryUtility(ITableauInstance)

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
            text = response.text
            text = text.encode(
                'ascii', errors="backslashreplace"
            ).decode('utf-8')
            xml_response = BeautifulSoup(text, 'xml')
            # Gets the token and site ID
            self.token = xml_response.find('credentials').get('token')
            self.site_id = xml_response.find('site').get('id')
            self.user_id = xml_response.find('user').get('id')
            result = self.token, self.site_id, self.user_id
        else:
            result = None
            logger.error("Cannot sign_in to [%s]. %s", url,
                         response.text)
        return result

    def sign_out(self):
        """
        Destroys the active session
        """
        if self.token:
            tableau = self.tableau
            url = "%s/api/%s/auth/signout" % (tableau.url, tableau.api_version)
            requests.post(url, headers={'x-tableau-auth': self.token})
            self.token = self.site_id = self.user_id = None
