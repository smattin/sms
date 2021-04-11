#!/bin/env -S python -u
#
import sys,logging
from string import digits,ascii_letters
from time import sleep, time
from queue import PriorityQueue
import random
import unittest

from message import Message
import options

phone_len = 10
max_msg_len = 100

# globals for monitoring
failed = 0
processing_time = 0; # double?

default={ 'messages': 1000
        , 'update_rate': 1
        , 'mean_processing_time': 5
        , 'failure_rate': 250 # per messages
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
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int # millisecs until delivery time
    item: Any=field(compare=False)

def sender( config=default):
    """
    picks up messages from the producer and
    simulates sending messages 

    N.B. not clear if distribution type is needed, assume uniform

    also has a configurable failure rate.
    """
    log = config['log']
    sending = PriorityQueue(config['messages'])
    message = Message().get()
    while not(message is None):
        # get message from queue, if any?

        log.debug('get message {}'.format(message.formatted()))
        secs = config['mean_processing_time'];

        # wait random time around mean_processing_time
        secs = config['mean_processing_time'];
        secs = random.uniform(0,2*secs)
        # instead of sleeping, just record absolute delivery time
        # and use priority queue for determining which should have been sent
        #   log.debug('sleep {} secs'.format(secs))
        #   sleep(secs)

        frate = config['failure_rate'] / config['messages']

        log.debug('message.send delay {}'.format(secs))
        message.send(secs,frate)

        ms = int((message.delivery - time())*1000)
        sending.put(PrioritizedItem(ms,message))

        message = Message().get()

    while not(sending.empty()):
        message = sending.get().item
        remaining = message.delivery - time()
        while 0 < remaining:
            log.debug('message {} secs remaining to send'.format(remaining))
            sleep(remaining)
            remaining = message.delivery - time()
        message.put()
        
if __name__ == '__main__':
    # get configuration values
    #     messages (number of) for producer
    #     update_rate for monitor
    #     mean_processing_time for sender
    #     failure_rate for sender
    #     
    config = options.get(sys.argv)
    log = config['log']

    sender(config)

