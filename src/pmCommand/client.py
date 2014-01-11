#
# Copyright (c) 2014, Mendix bv
# All Rights Reserved.
#
# http://www.mendix.com/
#

import xml.etree.ElementTree as et
import requests
from collections import OrderedDict
from log import logger
import structures


class ACSClient:

    def __init__(self, url):
        self._sid = None
        self._url = url
        self._headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def _wrap(self, action, subelements):
        # <avtrans>
        avtrans = et.Element("avtrans")
        # <sid>sid_if_logged_in</sid>
        sid = et.SubElement(avtrans, "sid")
        if self._sid is not None:
            sid.text = self._sid
        # <action>some_action</action>
        action_element = et.SubElement(avtrans, "action")
        action_element.text = action
        # <agents><src>wmi</src><dest>controller</dest></agents>
        agents = et.SubElement(avtrans, "agents")
        et.SubElement(agents, "src").text = "wmi"
        et.SubElement(agents, "dest").text = "controller"
        # wrap actual request
        avtrans.extend(subelements)
        # </avtrans>
        return avtrans

    def _request(self, action, subelements):
        avtrans = self._wrap(action, [subelements])
        xml = et.tostring(avtrans)
        logger.trace(">>> %s" % xml)
        response = requests.post(self._url, data=xml, headers=self._headers, verify=False)
        if (response.status_code != 200):
            logger.error("non-200 http status code: %s %s %s" %
                         response.status_code,
                         response.headers,
                         response.text)
            return None
        logger.trace("<<< %s" % response.text)
        return et.fromstring(response.text)

    def login(self, username, password):
        payload = et.Element("payload")
        payload_section = et.SubElement(payload, "section")
        payload_section.set("structure", "login")
        parameter_username = et.SubElement(payload_section, "parameter")
        parameter_username.set("id", "username")
        parameter_username.set("structure", "RWtext")
        et.SubElement(parameter_username, "value").text = username
        parameter_password = et.SubElement(payload_section, "parameter")
        parameter_password.set("id", "password")
        parameter_password.set("structure", "password")
        et.SubElement(parameter_password, "value").text = password

        response = self._request('login', payload)
        if response is None:
            return False

        sid = response.find("./sid").text
        logger.debug("Login successful, got sid: %s" % sid)
        self._sid = sid
        return True

    def listipdus(self):
        paths = et.Element("paths")
        et.SubElement(paths, "path").text = "units.powermanagement.pdu_management"

        response = self._request('get', paths)
        if response is None:
            return None

        ipdus = OrderedDict()
        for et_ipdu in response.findall("./payload/section[@id='pdu_devices_table']/array"):
            ipdus[et_ipdu.get("id")] = structures.PDU(et_ipdu)

        return ipdus
