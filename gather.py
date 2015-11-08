from scapy.all import *
from threading import Thread
from Queue import Queue
import sys
import json

from update_time import get_current_minute
from update_time import get_current_time
from devices import device

PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4
update_interval = 100 #minute
gathering_time = 60
<<<<<<< HEAD
pi_id = 1
=======
pi_id = 5
>>>>>>> fddd19ce69a245f5600ac4836618ff87e159e05c

device_list = []

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
            add2list(pkt)

def add2list(pkt):
    stre = -(256-ord(pkt.notdecoded[-4]))
    dev_found = False
    for dev in device_list:
        if pkt.addr2 == dev.mac_addr:
            dev.update(stre,get_current_minute(),get_current_time())
            dev_found = True
            break
    if dev_found == False:
        device_list.append(device(stre,get_current_minute(),get_current_time(),pkt.addr2))

def mac_gather(ifc):
    sniff(iface=ifc,prn=PacketHandler,timeout=gathering_time)

def del_outdated_device():
    current_time = get_current_minute()
    for dev in device_list:
        if(current_time - dev.last_detected_time > update_interval):
            device_list.remove(dev)

def upload_mac():
    time.sleep(gathering_time)
    #output to local file
    out = ''
    for dev in device_list:
        out = out + dev.myprint() +'\n'
    with open('/home/pi/rpi_sniff2.0/mac_addrs.txt','w') as out0:
        print >>out0,out

    #upload to server
    mac_list = []
    for dev in device_list:
        data = dict()
        data['no'] = pi_id
        data['mac'] = dev.mac_addr
        data['ssi'] = dev.strength
        data['time'] = dev.last_detected_time
        mac_list.append(data)
    #upload_post(data)
    with open ('/home/pi/rpi_sniff2.0/data.json','w') as f:
        json.dump(mac_list,f)

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
