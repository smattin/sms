import sys, getopt
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)
#log.setLevel(logging.DEBUG)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
log.addHandler(fh)

default={ 'messages': 1000
        , 'senders': 1
        , 'update_rate': 1
        , 'mean_processing_time': 5
        , 'failure_rate': 200
        , 'phone_len': 10
        , 'max_msg_len': 100
       } # TODO: get from ENV or file

def get(argv):
    """
    get command line options for SMS simulator
    """

    config=default

    help = argv[0] +' --help' \
                       +' --failure_rate (count/messages)' \
                       +' --mean_processing_time (secs)' \
                       +' --messages (count)' \
                       +' --update_rate (secs)' \
                       +' --senders (count)' \
                       +' --test' \
                       +' --debug'
    debug = False
    test = False

    try:
        opts, args = getopt.getopt(argv[1:],"hdtfmnps:",
        ["help","debug","test",
        "s=","senders=","n=","number=",
        "failure_rate=","m=","messages=","-p=","mean_processing_time=","update_rate="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)

    for opt,arg in opts:
        if opt in ['-h','--help']:
            print(help)
            sys.exit(0)

        if opt in ['-d','--debug']:
            debug=True
            log.setLevel(logging.DEBUG)

        if opt in ['-t','--test']:
            test = True

        if opt in ['-f','-fail','--failure_rate']:
            log.debug(arg)
            config['failure_rate'] = int(arg)
    
        if opt in ['-m','-msgs', '--messages']:
            config['messages'] = int(arg)

        if opt in ['-n','-num', '--number']:
            config['number'] = int(arg)

        if opt in ['-p','--mean_processing_time']:
            config['mean_processing_time'] = int(arg)
    
        if opt in ['-s','-send', '--senders']:
            config['senders'] = int(arg)
    
        if opt in ['-u','-update', '--update_rate']:
            config['update_rate'] = int(arg)
    
    log.debug(opts)
    config['log'] = log
    config['debug'] = debug
    config['test'] = test
    log.debug(config)
    return config

if __name__ == '__main__':
    options = get(sys.argv)
    log.debug(options)
