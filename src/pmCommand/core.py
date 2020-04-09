# Copyright 2014 Mendix
# MIT license, see LICENSE, see LICENSE

from pmCommand.client import ACSClient
from pmCommand.structures import PDU, Outlet
from pmCommand.log import logger


class PMCommand():

    def __init__(self):
        self.reload_config()

    def reload_config(self):
        self.client = ACSClient()

    def login(self, host, username, password):
        return self.client.login(host, username, password)

    def logout(self):
        return self.client.logout()

    def listipdus(self):
        return self.client.listipdus()

    def listipdus_table_info(self):
        return (PDU.fields, PDU.headers)

    def status(self, outlet_list=None):
        outlets = []
        if outlet_list is None:
            pdus = self.client.listipdus()
            for pdu in pdus:
                pdu_id = pdu.text['name']
                outlets.extend(self.client.outlets(pdu_id))
        else:
            too_many_outlets = []
            pdu_ids = set(map(lambda x: x[0], outlet_list))
            for pdu_id in pdu_ids:
                too_many_outlets.extend(self.client.outlets(pdu_id))
            for pdu_id, outlet_id in outlet_list:
                outlets.extend(
                    filter(lambda x: x.text['outlet'] == "%s[%s]" %
                           (pdu_id, outlet_id), too_many_outlets)
                )

        return outlets

    def status_table_info(self):
        return (Outlet.fields, Outlet.headers)

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
            logger.info("Saving configuration on PDU %s." % pdu.text['name'])
            self.client.save(pdu.text['name'])

    def get_session_idle_timeout(self):
        return self.client.get_session_idle_timeout()
