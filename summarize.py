#!/bin/env -S python -u
#
import sys,logging
from string import digits,ascii_letters

import random
import unittest

from message import Message

# TODO: extract this log config logic
log = logging.getLogger()
log.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
log.addHandler(fh)

phone_len = 10
max_msg_len = 100

# globals for monitoring
sent = 0
failed = 0
total_time = 0.0; # double?

default={ 'messages': 1000
        , 'update_rate': 1
        , 'mean_total_time': 5
        , 'failure_rate': 250 # per messages
       } # TODO: get from ENV or file

def summarize( config ):
    """
    summarize the SMS status
    """

    sent = 0
    failed = 0
    total_time = 0.0
    while True:
        message = Message().get()
        if message is None:
            break
        else:

            status = message.status.name
            if 'UNSENT' != status:
                sent = sent + 1
                failed = failed + 1 if 'FAILED' == status else failed
                ptime = message.delay if hasattr(message,'delay') else 0.0
                total_time = total_time + float(ptime)
                print('sent {} messages, {} failed, {} secs/msg'.format(sent,failed,round(total_time/sent,2)))
            else:
                break

if __name__ == '__main__':
    # get configuration values
    #     messages (number of) for producer
    #     update_rate for monitor
    #     mean_total_time for sender
    #     failure_rate for sender
    #     
    argc = len(sys.argv)
    if ('-d' in sys.argv):
        log.setLevel(logging.DEBUG)
        argc = argc -1

    config = default
    log.debug(sys.argv)
    if 1 < argc:
        config['update_rate'] = int(sys.argv[len(sys.argv)-1])

    log.debug(config)
    summarize(config)
