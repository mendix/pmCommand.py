# Copyright 2014 Mendix
# MIT license, see LICENSE, see LICENSE

import logging
import pmCommand
import re

pdu_outlet_regex = re.compile(r'^(?P<pdu_id>[\w-]+)\[(?P<outlet_id>\d+)\]$')


def parse_outlet(pdu_outlet):
    match = pdu_outlet_regex.match(pdu_outlet)
    if match is None:
        raise pmCommand.Error("Invalid outlet: {}".format(pdu_outlet))
    groupdict = match.groupdict()
    return groupdict['pdu_id'], groupdict['outlet_id']


def print_table(devices, sort=True, output_filters=None):
    if output_filters is None:
        output_filters = {}

    def apply_output_filter(device, attr):
        if attr not in output_filters:
            return device.values[attr]
        return output_filters[attr](device, attr)

    if len(devices) == 0:
        logging.info("Empty result, nothing to show.")
        return

    if sort:
        devices = sorted(devices)

    print()

    output = ['']
    maxlen = {}

    # Just assume all objects in devices are of equal type (like, all PDUs or
    # all Outlets and have the same fields to show. Use the field names from
    # the first one to look at all column headers and actual values to find the
    # longest one.
    attrs = devices[0].headers.keys()
    for attr in attrs:
        maxlen[attr] = max(len(devices[0].headers[attr]),
                           max([len(apply_output_filter(device, attr))
                                for device in devices]))
        output.append(devices[0].headers[attr].ljust(maxlen[attr]))
    print('  '.join(output))

    output = ['']
    for attr in attrs:
        output.append('=' * maxlen[attr])
    print('  '.join(output))

    for device in devices:
        output = ['']
        for attr in attrs:
            output.append(apply_output_filter(device, attr).ljust(maxlen[attr]))
        print('  '.join(output))

    print()
