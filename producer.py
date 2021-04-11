#!/bin/env -S python
#
import sys,logging
from string import digits,ascii_letters
from time import sleep

import random
import unittest

from message import Message
import options

phone_len = 10
max_msg_len = 100

# globals for monitoring
sent = 0
failed = 0
processing_time = 0; # double?

default={ 'messages': 1000
        , 'update_rate': 1
        , 'mean_processing_time': 1
        , 'failure_rate': 1
       } # TODO: get from ENV or file

# def simulator(config):
"""
    The objective is to simulate sending a large number of SMS alerts,
    like for an emergency alert service.

    The simulation consists of three parts:

        A producer that generates a configurable number of messages (default 1000)
    to random phone number. Each message contains up to 100 random characters.

        A sender, who picks up messages from the producer and
    simulates sending messages by waiting a random period time
    distributed around a configurable mean.
    The sender also has a configurable failure rate.

        A progress monitor that displays the following and
    updates it every N seconds (configurable):


    One instance each for the  producer and the progress monitor will be started
    while a variable number of senders can be started with
    different mean processing time and error rate settings.

    You are free in the programming language you choose,
    but your code should come with reasonable unit testing.

    commercial simulator: https://melroselabs.com/services/smsc-simulator/
"""

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

