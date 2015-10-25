#!/usr/bin/python

import os
import subprocess
import time


fail_count = 0
f = open('/home/pi/rpi_sniff2.0/log.txt','a')

while(1):
    s = os.popen("ifconfig").read()
    if 'ppp0' in s:
        s = os.popen("poff shinez")
    if '172.26' in s:
        s = os.popen("dhclient wlan0 -r")
    s = os.popen("ifconfig wlan0 down")
    time.sleep(1)
    #ensure wlan0 Monitor
    while(fail_count<=3):
        s = os.popen("iwconfig wlan0 mode monitor")
        res = os.popen("iwconfig").read()
        if 'Monitor' in res:
            fail_count = 0
            print >>f,"successed to switching to monitor mode"
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        print >>f,"failed to switching to monitor mode"
        f.close()
        time.sleep(59)
        s = os.popen("reboot")
    s = os.popen("ifconfig wlan0 up")
    time.sleep(0.5)
    #start sniff
    subprocess.call("/usr/bin/python /home/pi/rpi_sniff2.0/gather.py",shell = True)
    #os.call("/usr/bin/python /home/pi/rpi_sniff2.0/gather.py")
    #time.sleep(65)
    s = os.popen("ifconfig wlan0 down")
    #ensure wlan0 Managed
    while(fail_count<=3):
        s = os.popen("iwconfig wlan0 mode managed")
        time.sleep(1)
        res = os.popen("iwconfig").read()
        if 'Managed' in res:
            fail_count = 0
            print >>f,"successed to switching to managed mode"
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        print >>f,"failed to switch to managed mode"
        f.close()
        time.sleep(59)
        s = os.popen("reboot")
    s = os.popen("iwconfig wlan0 essid NJU-WLAN")
    time.sleep(1)
    s = os.popen("ifconfig wlan0 up")
    time.sleep(2)
    #ensure wifi connected
    while(fail_count<=3):
        s = os.popen("iwconfig").read()
        if 'Not-Associated' in s:
            fail_count += 1
            s = os.popen("iwconfig wlan0 essid NJU-WLAN")
            time.sleep(1)
            s = os.popen("ifconfig wlan0 up")
            time.sleep(2)
        else:
            fail_count = 0
            print >>f,"successed to connected wifi"
            break
    if(fail_count>=3):
        print >>f,"failed to connect wifi"
        f.close()
        time.sleep(59)
        s = os.popen("reboot")
    #ensure gain ip
    while(fail_count<=3):
        s = os.popen("ifconfig").read()
        if '172.26' in s:
            fail_count = 0
            print >>f,"successed to gain ip"
            break
        else:
            fail_count += 1
            s = os.popen("dhclient wlan0")
            time.sleep(1)
    if(fail_count>=3):
        print >>f,"failed to gain ip"
        f.close()
        time.sleep(59)
        s = os.popen("reboot")
    #ensure connect vpn:
    while(fail_count<=3):
        s = os.popen("pon shinez")
        time.sleep(1)
        s = os.popen("ifconfig").read()
        if 'ppp0' in s:
            fail_count = 0
            print >>f,"successed to connected vpn"
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        print >>f,"failed to connect vpn"
        f.close()
        time.sleep(59)
        s = os.popen("reboot")
    #set route
    s = os.popen("ip route del default")
    time.sleep(3)
    while(fail_count<=3):
        s = os.popen("ip route add default dev ppp0").read()
        #s = os.popen("route add default gw 192.168.9.1").read()
        time.sleep(0.3)
        s = os.popen("ip route").read()
        if 'default' in s:
            print s
            print >>f,"successed to set route"
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        print >>f,"failed to set route"
        f.close()
        time.sleep(59)
        s = os.popen("reboot")
    #send
    #s = subprocess.call("/usr/bin/python /home/pi/rpi_sniff2.0/send_mail.py",shell = True)
    s = subprocess.call("/usr/bin/python /home/pi/rpi_sniff2.0/upload.py",shell = True)
    #time.sleep(10)

