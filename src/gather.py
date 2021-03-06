from scapy.all import *
from threading import Thread
import json

from pitime import get_current_minute
from pitime import get_current_time
from devices import device
from config import *

PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4

device_list = []

gather_c = conf()
work_dir = gather_c.work_dir

def packet_handler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
            add2list(pkt)


def add2list(pkt):
    stre = -(256-ord(pkt.notdecoded[-4]))
    dev_found = False
    for dev in device_list:
        if pkt.addr2 == dev.mac_addr:
            dev.update(stre,get_current_minute(), get_current_time())
            dev_found = True
            break
    if not dev_found:
        device_list.append(device(stre, get_current_minute(), get_current_time(), pkt.addr2))


def mac_gather(ifc):
    sniff(iface=ifc, prn=packet_handler, timeout=c.gathering_time)


def del_outdated_device():
    current_time = get_current_minute()
    for dev in device_list:
        if current_time - dev.last_detected_time > c.update_interval:
            device_list.remove(dev)


def dump_mac_addr():
    local_log_file = work_dir + 'mac_addrs.txt'
    json_file = work_dir + 'data.json'

    time.sleep(c.gathering_time)
    # output to local log file
    out_content = ''
    for dev in device_list:
        out_content = out_content + dev.myprint() + '\n'
    with open(local_log_file, 'w') as log_file:
        print >> log_file, out_content
    print out_content

    # dump to json file
    mac_list = []
    for dev in device_list:
        data = dict()
        data['no'] = c.pi_id
        data['mac'] = dev.mac_addr
        data['ssi'] = dev.strength
        data['time'] = dev.last_detected_time
        mac_list.append(data)

    with open (json_file, 'w') as f:
        json.dump(mac_list, f)


def main():
    c.init()
    threads = []

    gather_thread = Thread(target = mac_gather,args=('wlan1',))
    gather_thread.start()
    threads.append(gather_thread)

    upload_thread = Thread(target = dump_mac_addr)
    upload_thread.start()
    threads.append(upload_thread)

    for t in threads:
        t.join()


if __name__ =='__main__':
    main()
