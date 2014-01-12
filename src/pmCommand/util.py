from log import logger
import re

pdu_outlet_regex = re.compile(r'^(?P<pdu_id>\w+)\[(?P<outlet_id>\d+)\]$')


def parse_outlet(pdu_outlet):
    match = pdu_outlet_regex.match(pdu_outlet)
    if match is None:
        logger.error("Invalid outlet: %s" % pdu_outlet)
        return (None, None)
    groupdict = match.groupdict()
    return (groupdict['pdu_id'], groupdict['outlet_id'])


def remove_outlet_crap(outlet_name):
    return '_'.join(outlet_name.split('_')[:-1])