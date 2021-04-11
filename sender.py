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

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int # millisecs until delivery time
    item: Any=field(compare=False)

def input(sender):
    return "sender"+str(sender)+".txt"

messageInput = sys.stdin
def getMessage():
    global messageInput
    message = None
    if 1 < config['senders'] and messageInput == sys.stdin:
        my = config['number']
        log.debug('opening message input {}'.format(input(my)))
        messageInput = open(input(my), 'r')
    return Message().get(messageInput)

def sender( config=options.default):
    """
    picks up messages from the producer and
    simulates sending messages 

    N.B. not clear if distribution type is needed, assume uniform

    also has a configurable failure rate.
    """
    log = config['log']
    sending = PriorityQueue(config['messages'])

    message = getMessage()
    while not(message is None):

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

        log.debug('sender {} queue size {} messages'.format(config['number'],sending.qsize()))
        message = getMessage()

    messageInput.close();
    log.debug('sender {} queue size {} messages'.format(config['number'],sending.qsize()))
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
    log.debug(config)

    sender(config)

