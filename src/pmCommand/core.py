# Copyright (c) 2009-2013, Mendix bv
# All Rights Reserved.
# http://www.mendix.com/
#

from client import ACSClient
from structures import PDU


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
