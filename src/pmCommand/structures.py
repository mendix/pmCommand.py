# Copyright 2014 Mendix
# MIT license, see LICENSE, see LICENSE


class DeviceFromXML:
    def __init__(self, et_array):
        self.headers = {}  # description, useful as column header
        self.values = {}

        for et_param in et_array.findall("./parameter"):
            param_id = et_param.get("id")  # e.g. pduId_Index
            header = et_param.get("label")
            if header is None:
                continue  # hidden, e.g. the 'thresholds' field of an ipdu
            self.headers[param_id] = et_param.get("label")
            et_value = et_param.find("./value")
            self.values[param_id] = et_value.get("label")

    def __getattr__(self, attr):
        if attr in self.values:
            return self.values[attr]
        else:
            raise AttributeError


class PDU(DeviceFromXML):
    """
    Load PDU information from an XML PDU object

    Known attributes (all are stored as text):

    Attribute     Header              Example value
    =========     ===========         =======
    pduId_Index   PDU ID              power3-r17
    pdu_vendor    Vendor              Avocent
    pdu_model     Model               PM3000/10/16A
    pdu_pos       Position            ttyS4/1

    (when connecting via a Cyclades ACS)
    pdu_status    Status              On Line
    pdu_outlets   Outlets (On/Total)  8/10

    (when connecting directly to a PM)
    pdu_status    Status (On/Total)   8/10

    pdu_current   Current (A)         4.2
    pdu_power     Power (W)           1002.0
    pdu_alarm     Alarm               Normal
    """
    def __init__(self, et_pdu):
        super().__init__(et_pdu)

    def __lt__(self, other):
        return self.pduId_Index < other.pduId_Index


class Outlet(DeviceFromXML):
    """
    Load Outlet information

    Known attributes (all are stored as text):

    Attribute        Header         Example value
    =========        ===========    =======
    outlet_number    Outlet         6
    outlet_name      Name           HE20-flapsie-L
    status           Status         ON(locked)
    circuit          Bank           N/A
    outlet_current   Current (A)    0.4
    outlet_power     Power (W)      110.0
    """
    def __init__(self, et_outlet, pdu_id):
        super().__init__(et_outlet)
        self.pdu_id = pdu_id  # for sorting purposes

    def __lt__(self, other):
        return (self.pdu_id, int(self.outlet_number)) < \
            (other.pdu_id, int(other.outlet_number))
