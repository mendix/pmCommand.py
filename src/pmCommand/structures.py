# Copyright 2014 Mendix
# MIT license, see LICENSE, see LICENSE
from pmCommand.log import logger


class PDU(object):

    fields = ('name', 'vendor', 'model', 'position', 'status',
              'outlets', 'current', 'power', 'alarm')

    headers = {}

    def __init__(self, et_pdu):
        mapping = [
            ("pduId_Index", "name"),
            ("pdu_vendor", "vendor"),
            ("pdu_model", "model"),
            ("pdu_pos", "position"),
            ("pdu_status", "status"),
            ("pdu_outlets", "outlets"),
            ("pdu_current", "current"),
            ("pdu_power", "power"),
            ("pdu_alarm", "alarm"),
        ]
        (self.text, self.label) = load_array(et_pdu, PDU.headers, mapping)

    def __lt__(self, other):
        return self.text['name'] < other.text['name']


class Outlet(object):

    fields = ('outlet', 'name', 'status', 'current')

    headers = {}

    def __init__(self, et_outlet, pdu_id):
        mapping = [
            ("outlet_number", "number"),
            ("outlet_name", "name"),
            ("status", "status"),
            ("outlet_current", "current"),
            ("outlet_power", "power"),
        ]
        (self.text, self.label) = load_array(et_outlet, Outlet.headers, mapping)

        Outlet.headers['outlet'] = "Outlet"
        self.text['outlet'] = "%s[%s]" % (pdu_id, self.text['number'])
        self.label['outlet'] = self.text['outlet']

        self.text['name'] = self.label['name']
        self.label['name'] = self.text['name']

        self.pdu_id = pdu_id

    def __lt__(self, other):
        return ((self.pdu_id, int(self.text['number'])) <
                (other.pdu_id, int(other.text['number'])))


def load_array(et_array, headers, mapping):

    text = {}
    label = {}

    for them, us in mapping:
        et_param = et_array.find("./parameter[@id='%s']" % them)
        et_value = et_param.find("./value")

        text[us] = et_value.text
        label[us] = et_value.get("label")

        header = et_param.get("label")
        current_header = headers.setdefault(us, header)
        if current_header != header:
            logger.warn("Different header for new row detected: %s -> %s"
                        % (current_header, header))

    return (text, label)
