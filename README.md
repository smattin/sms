# sms
SMS simulator for emergency alert system

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

    A commercial simulator: https://melroselabs.com/services/smsc-simulator/
