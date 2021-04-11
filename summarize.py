#!/bin/env -S python -u
#
import sys,logging
from string import digits,ascii_letters

import random
import unittest

import options
from message import Message

def summarize( config ):
    """
    summarize the SMS status
    """

    sent = 0
    failed = 0
    total_time = 0.0
    while True:
        message = Message().get() # TODO: Get from multiple sender output
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

    config = options.get(sys.argv)
    log = config['log']

    log.debug(config)
    summarize(config)
