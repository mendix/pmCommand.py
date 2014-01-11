class PDU(object):

    def __init__(self, et_ipdu):
        self.ipdu_id = et_ipdu.get("id")
        self.vendor = et_ipdu.find("./parameter[@id='pdu_vendor']/value").text
        self.model = et_ipdu.find("./parameter[@id='pdu_model']/value").text
        self.pos = et_ipdu.find("./parameter[@id='pdu_pos']/value").text
        self.status = et_ipdu.find("./parameter[@id='pdu_status']/value").text
        self.outlets = et_ipdu.find("./parameter[@id='pdu_outlets']/value").text
        self.current = et_ipdu.find("./parameter[@id='pdu_current']/value").text
        self.power = et_ipdu.find("./parameter[@id='pdu_power']/value").text
        self.alarm = et_ipdu.find("./parameter[@id='pdu_alarm']/value").text
