import os
import collections
import time

Interface =  collections.namedtuple('Interface', ['name', 'tx_bytes', 'rx_bytes'])

def read_data():
    interfaces = {}
    for name in os.listdir('/sys/class/net/'):
        stats_path = '/sys/class/net/{}/statistics'.format(name)
        tx_bytes = 0
        rx_bytes = 0
        with open('{}/rx_bytes'.format(stats_path)) as f:
            rx_bytes = int(f.readline())
        with open('{}/tx_bytes'.format(stats_path)) as f:
            tx_bytes = int(f.readline())
        interfaces[name] = Interface(name, tx_bytes, rx_bytes)
    return interfaces

def printer(interface):
    text = 'Interface:{}\tUpload:{}\tDownload:{}\t' 
    print(text.format(interface.name, format_bytes(interface.tx_bytes), format_bytes(interface.rx_bytes)))

def format_bytes(value):
    final_value = 0
    metric = ''
    if value < 1000:
        final_value = value
        metric = 'Bs'
    elif value >= 1000 and value < 1000000:
        final_value = value / 1000
        metric = 'kBs'
    else:
        final_value = value / 1000000
        metric = 'mBs'
    return '{}/{}'.format(final_value, metric)

def check_diff(old, new):
    tx_bytes = new.tx_bytes - old.tx_bytes
    rx_bytes = new.rx_bytes - old.rx_bytes
    return Interface(new.name, tx_bytes, rx_bytes)

while(True):
    interfaces = read_data()
    time.sleep(1)
    new_interfaces = read_data() 
    for key in new_interfaces.keys():
        printer(check_diff(interfaces[key], new_interfaces[key]))

