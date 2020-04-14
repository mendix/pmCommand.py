# Copyright 2014 Mendix
# MIT license, see LICENSE, see LICENSE

import pmCommand
import re

pdu_outlet_regex = re.compile(r'^(?P<pdu_id>[\w-]+)\[(?P<outlet_id>\d+)\]$')


def parse_outlet(pdu_outlet):
    match = pdu_outlet_regex.match(pdu_outlet)
    if match is None:
        raise pmCommand.Error("Invalid outlet: {}".format(pdu_outlet))
    groupdict = match.groupdict()
    return groupdict['pdu_id'], groupdict['outlet_id']
