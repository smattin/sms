import sys,logging
from string import digits,ascii_letters
from time import time
import random
import unittest
from io import StringIO
from enum import Enum, unique

import options

phone_len = 10
max_msg_len = 100

class Status(Enum):
    """
        message status is UNSENT initially, then SENT or FAILED
    """
    UNSENT = 'initial status'
    SENT = 'message was sent successfully'
    FAILED = 'message sending failed'

class Message:

    sep = ','

    def __init__(self,phone='',text='',status=Status.UNSENT):
        """ 100 random characters """
        #chars = string.printable
        chars = ascii_letters+digits # not including whitespace initially
        self.text = text if 0<len(text) else ''.join(random.choice(chars)
                for i in range(random.randint(1,max_msg_len)))
        self.phone = phone if 0<len(phone) else ''.join(random.choice(digits)
                for i in range(10))
        self.status = status

    def formatted(self):
        fields = [str(self.status.name), self.phone, self.text]
        if hasattr(self,'delay') and 0 < self.delay:
            fields.append(str(self.delay))
        return Message.sep.join(fields)

    def send(self,delay=0.0,frate=0.0):
        self.delay = delay
        self.delivery = time() + delay

        [failure] = random.choices([True,False],[frate,1-frate])

        self.status = Status.SENT if not(failure) else Status.FAILED

    def put(self,output=sys.stdout):
        msg = self.formatted()
        if output==sys.stdout:
            print(msg)
        else:
            with open(output, 'w') as f:
                print(msg,file=f)

    def get(self,input=sys.stdin): # get from input in same format as put
        line = input.readline()
        values = line.rstrip().split(Message.sep)

        if 2 < len(values):
            self.status = Status[values[0]]
            self.phone = values[1]
            self.text = values[2]
            #self.__init__(values[0],values[1])
            if 3 < len(values):
                self.delay = values[3]
        else:
            return None

        return self

class TestMessage(unittest.TestCase):

    data = u"""\
UNSENT,0520714475,U6zEmEjGOiuNQTnj4LmJkAX0qsFIDy7CLgmobHVtVE5wEVFCvOo
UNSENT,2034635684,rOFZUPpszJIdMv3RAMLkM7Ase6i3gOgUiVb7ZfKVA7zbpiGHR974fzdw5ZXuvLnFd4Hq0xyVZIPpD0DikQdeYgFy
UNSENT,8492886373,pb8gp29LoXeCmbAZv4Tzzw
UNSENT,6125089266,AC0XsoGpZBROdocH8Chp8HyP3EKCOpP2I4eGn3JcO4aT7N
FAILED,9782268322,DgOVY6OQG5Kjj
"""

    def test0(self):
        m = Message()
        log.debug(m)
        text = m.text
        phone = m.phone

        #self.assertTrue(isinstance(phone,str))
        self.assertTrue(isinstance(text,str))

        self.assertEqual(len(phone),phone_len)
        self.assertTrue(0<len(text))
        self.assertTrue(len(text)<=max_msg_len)

    def test1(self):

        m = Message().get(StringIO(TestMessage.data))
        log.debug(m)

        self.assertTrue(not(m is None))
        self.assertEqual(520714475,int(m.phone))

    def test2(self):
        input = StringIO(TestMessage.data);
        
        msgs = [Message().get(input),
                Message().get(input),
                Message().get(input),
                Message().get(input),
                Message().get(input)]

        self.assertEqual(5,len(msgs))
        self.assertNotIn(None,msgs)
        self.assertEqual(None,Message().get(input))

    def test3(self):
        testfile = 'msg.txt'
        m = Message().get(StringIO(TestMessage.data))
        m.put(testfile)
        with open(testfile, 'r') as f:
            line = f.readline()
            self.assertEqual(m.formatted(),line.rstrip())

    def test4(self):
        testfile = 'msg.txt'
        m = Message().get(StringIO(TestMessage.data))
        m.send(1.0,0.1)
        self.assertIn(m.status,[Status.SENT,Status.FAILED])
        now = time()
        self.assertGreater(m.delivery,now)

if __name__ == '__main__':
    global config
    global log
    config = options.get(sys.argv)
    log = config['log']
    if config['test']:
        suite = unittest.TestSuite()
        for n in range(5):
            suite.addTest(TestMessage('test'+str(n)))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        exit(0 if result.wasSuccessful() else 1)
        # unittest.main(argv=['first-arg-is-ignored'], exit=False)

    Message().put()

