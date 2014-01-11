from log import logger


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
