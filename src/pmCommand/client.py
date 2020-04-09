# Copyright 2014 Mendix
# MIT license, see LICENSE, see LICENSE

import xml.etree.ElementTree as et
import requests
from pmCommand.log import logger
import pmCommand.structures as structures


class ACSClient:

    def __init__(self):
        self._sid = None
        self._url = None
        self._headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def _wrap(self, action, path=None, pathvar=None, payload=None):
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
        if path is not None:
            # <paths><path>foo.bar</path><pathvar>baz</pathvar></paths>
            et_paths = et.SubElement(avtrans, "paths")
            et.SubElement(et_paths, "path").text = path
            if pathvar is not None:
                et.SubElement(et_paths, "pathvar").text = pathvar
        # wrap actual request
        if payload is not None:
            et_payload = et.SubElement(avtrans, "payload")
            et_payload.append(payload)
        # </avtrans>
        return avtrans

    def _request(self, action, path=None, pathvar=None, payload=None):
        if self._url is None:
            raise RuntimeError("Please login first.")

        avtrans = self._wrap(action, path, pathvar, payload)
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
        et_response = et.fromstring(response.text)
        et_error = et_response.find("./error")
        if et_error is not None:
            logger.error(et_error.get("label"))

        if ((et_response.find("./action").text == "login"
             and action != "login" and action != "logout")):
            self._sid = None
            raise RuntimeError("Invalid session, please login first.")

        return et_response

    def login(self, host, username, password):
        self._url = "https://%s/appliance/avtrans" % host
        logger.debug("Logging into url %s as %s" % (self._url, username))

        et_section = et.Element("section")
        et_section.set("structure", "login")
        parameter_username = et.SubElement(et_section, "parameter")
        parameter_username.set("id", "username")
        parameter_username.set("structure", "RWtext")
        et.SubElement(parameter_username, "value").text = username
        parameter_password = et.SubElement(et_section, "parameter")
        parameter_password.set("id", "password")
        parameter_password.set("structure", "password")
        et.SubElement(parameter_password, "value").text = password

        response = self._request('login', payload=et_section)
        if response is None:
            return False

        sid = response.find("./sid").text
        if sid is None:
            return False
        logger.debug("Login successful, got sid: %s" % sid)
        self._sid = sid
        return True

    def logout(self):
        et_response = self._request(action="logout")
        if (et_response.find("./action").text == "login"):
            logger.info("Logout successful.")
            self._sid = None
            return True
        # haven't seen any way yet to end up here
        return False

    def listipdus(self):
        et_response = self._request(action="get",
                                    path="units.powermanagement.pdu_management")
        et_ipdus = et_response.findall("./payload/section[@id='pdu_devices_table']/array")
        return [structures.PDU(et_ipdu) for et_ipdu in et_ipdus]

    def outlets(self, pdu_id):
        et_response = self._request(
            action="get",
            path="units.powermanagement.pdu_management.pduDevicesDetails.outletTable",
            pathvar=pdu_id
        )
        et_outlets = et_response.findall("./payload/section[@id='outlet_details']/array")
        return [structures.Outlet(et_outlet, pdu_id) for et_outlet in et_outlets]

    def outlet_action(self, action, pdu_id, outlet_id):
        et_section = et.Element("section")
        et_section.set("structure", "table")
        et_section.set("id", "outlet_details")
        et_array = et.SubElement(et_section, "array")
        et_array.set("id", outlet_id)

        et_response = self._request(
            action=action,
            path="units.powermanagement.pdu_management"
                 ".pduDevicesDetails.outletTable.Nazca_outlet_table",
            pathvar=pdu_id,
            payload=et_section
        )
        et_outlet = et_response.find("./payload/section[@id='outlet_details']"
                                     "/array[@id='%s']" % outlet_id)
        if et_outlet is None:
            logger.error("Outlet %s[%s] not found." % (pdu_id, outlet_id))
        else:
            outlet_name = et_outlet.find("./parameter[@id='outlet_name']/value").text
            outlet_status = et_outlet.find("./parameter[@id='status']/value").text
            logger.info("%s[%s]: status of outlet %s is now: %s" %
                        (pdu_id, outlet_id, outlet_name, outlet_status))

    def save(self, pdu_id):
        et_section = et.Element("section")
        et_section.set("structure", "table")
        et_section.set("id", "outlet_details")

        self._request(
            action="savepdu",
            path="units.powermanagement.pdu_management.pduDevicesDetails"
                 ".outletTable.Nazca_outlet_table",
            pathvar=pdu_id,
            payload=et_section
        )

    def get_session_idle_timeout(self):
        et_response = self._request(
            action="get",
            path="units.applianceSettings.security.SecurityProfileNav"
        )
        return int(et_response.find("./payload/section[@id='securityProfile']"
                                    "/parameter[@id='sessionTimeout']"
                                    "/parameter[@id='idletimeout']/value").text)
