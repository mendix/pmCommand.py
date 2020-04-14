# Copyright 2014 Mendix
# MIT license, see LICENSE, see LICENSE

import logging
from pmCommand.client import ACSClient


class PMCommand():

    def __init__(self):
        self.reload_config()

    def reload_config(self):
        self.client = ACSClient()

    def login(self, baseurl, username, password):
        self.welcome, self.product = self.client.login(baseurl, username, password)

    def logout(self):
        self.client.logout()

    def listipdus(self):
        return self.client.listipdus()

    def status(self, outlet_list=None):
        """
        The arg outlet_list is either omitted (None) or a list of tuples with
        (pdu_id, outlet_number), like ('power3', '7').

        The return value is a dictionary which has the same kind of tuples as
        keys and the actual Outlet objects as values.
        """
        result = {}
        if outlet_list is None:
            pdus = self.client.listipdus()
            for pdu in pdus:
                for outlet in self.client.outlets(pdu.pduId_Index):
                    result[(pdu.pduId_Index, outlet.outlet_number)] = outlet
        else:
            # which pdu collection do we need outlet info from?
            pdu_ids = set([_[0] for _ in outlet_list])
            # for each pdu, get all outlets and only add requested ones to result
            for pdu_id in pdu_ids:
                for outlet in self.client.outlets(pdu_id):
                    if (pdu_id, outlet.outlet_number) in outlet_list:
                        result[(pdu_id, outlet.outlet_number)] = outlet
        return result

    def on(self, pdu_id, outlet_id):
        return self.outlet_action("on", pdu_id, outlet_id)

    def off(self, pdu_id, outlet_id):
        return self.outlet_action("off", pdu_id, outlet_id)

    def lock(self, pdu_id, outlet_id):
        return self.outlet_action("lock", pdu_id, outlet_id)

    def unlock(self, pdu_id, outlet_id):
        return self.outlet_action("unlock", pdu_id, outlet_id)

    def cycle(self, pdu_id, outlet_id):
        return self.outlet_action("cycle", pdu_id, outlet_id)

    def outlet_action(self, action, pdu_id, outlet_id):
        return self.client.outlet_action(action, pdu_id, outlet_id)

    def save(self):
        for pdu in self.client.listipdus():
            logging.info("Saving configuration on PDU {}.".format(pdu.text['name']))
            self.client.save(pdu.text['name'])

    def get_session_idle_timeout(self):
        return self.client.get_session_idle_timeout()
