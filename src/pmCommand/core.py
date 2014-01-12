# Copyright (c) 2009-2013, Mendix bv
# All Rights Reserved.
# http://www.mendix.com/
#

from client import ACSClient
from structures import PDU, Outlet


class PMCommand():

    def __init__(self):
        self.reload_config()

    def reload_config(self):
        self.client = ACSClient("https://10.140.11.30/appliance/avtrans")

    def login(self, username, password):
        return self.client.login(username, password)

    def listipdus(self):
        return self.client.listipdus()

    def listipdus_table_info(self):
        return (PDU.fields, PDU.headers)

    def status(self):
        pdus = self.client.listipdus()
        outlets = []
        for pdu in pdus:
            pdu_id = pdu.text['name']
            outlets.extend(self.client.outlets(pdu_id))
        return outlets

    def status_table_info(self):
        return (Outlet.fields, Outlet.headers)

    def on(self, pdu_id, outlet_id):
        return self.outlet_action("on", pdu_id, outlet_id)

    def outlet_action(self, action, pdu_id, outlet_id):
        return self.client.outlet_action(action, pdu_id, outlet_id)
