from log import logger


class PDU(object):

    headers = {}

    def __init__(self, et_pdu):
        self.text = {}
        self.label = {}

        for them, us in [
            ("pduId_Index", "name"),
            ("pdu_vendor", "vendor"),
            ("pdu_model", "model"),
            ("pdu_pos", "position"),
            ("pdu_status", "status"),
            ("pdu_outlets", "outlets"),
            ("pdu_current", "current"),
            ("pdu_power", "power"),
            ("pdu_alarm", "alarm"),
        ]:
            et_param = et_pdu.find("./parameter[@id='%s']" % them)
            et_value = et_param.find("./value")

            self.text[us] = et_value.text
            self.label[us] = et_value.get("label")

            header = et_param.get("label")
            current_header = PDU.headers.setdefault(us, header)
            if current_header != header:
                logger.warn("PDU: different header for new row detected: %s -> %s"
                            % (current_header, header))
