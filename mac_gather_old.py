from scapy.all import *
from update_time import get_current_minute
from mac_upload import mac_data_packet

from threading import Thread
from Queue import Queue

import sys

PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4

mac_list = []
mac_last_update_time = dict()
update_interval = 10 #minute
old_time = 0
mac_queue = Queue()

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
            add2list(pkt)
       # current_time = get_current_minute()

       # global old_time
       # if((current_time - old_time) > update_interval):
       #     old_time = current_time
       #     upload_mac()

def add2list(pkt):
    mac_strength = -(256-ord(pkt.notdecoded[-4:-3]))
    if ((pkt.addr2,mac_strength) in mac_list) == 0:
        mac_list.append((pkt.addr2,mac_strength))
    mac_last_update_time[pkt.addr2] = get_current_minute()
    current_time = get_current_minute()


def get_current_mac_list():
    current_time = get_current_minute()
    for entry in mac_list:
        mac_addr,mac_str = entry
        if(current_time - mac_last_update_time[mac_addr] > update_interval):
            del mac_last_update_time[mac_addr]
            mac_list.remove(entry)
    return mac_list

def mac_gather(ifc):
    sniff(iface=ifc,prn=PacketHandler)

def upload_mac():
    while(1):
        time.sleep(3)
        print mac_data_packet(get_current_mac_list())

def main():
    threads = []

    gather_thread = Thread(target = mac_gather,args=('wlan0',))
    gather_thread.start()
    threads.append(gather_thread)

    upload_thread = Thread(target = upload_mac)
    upload_thread.start()
    threads.append(upload_thread)

    for t in threads:
        t.join()

if __name__ =='__main__':
    main()
