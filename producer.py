#!/bin/env -S python
#
from string import digits,ascii_letters
from time import sleep

import unittest

from message import Message
import options

phone_len = 10
max_msg_len = 100

# globals for monitoring
sent = 0
failed = 0
processing_time = 0; # double?

def producer(messages=1000):
    """
    generate a configurable number of messages (default 1000)
    to random phone number. Each message contains up to 100 random characters.
    
    cloud producer might be AWS Lamda to SQS

    outputs messages as lines to stdout formatted like: phone <tab> text
    """
    while (0 < messages):
        # do we really care about phone number?
        # get message

        m = Message()
        m.put() # allow file descriptor?
        # put in queue like SQS FIFO https://aws.amazon.com/sqs/
        #     $0.50 per million API requests
        #     msg.put(m)
        messages = messages - 1

if __name__ == '__main__':
    # get configuration values
    #     messages (number of) for producer
    #     update_rate for monitor
    #     mean_processing_time for sender
    #     failure_rate for sender
    #     
    global config
    global log
    config = options.get(sys.argv)
    log = config['log']
    log.debug(config)
    producer(config['messages'])

