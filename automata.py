#!/usr/bin/python

import os
import subprocess
import time


fail_count = 0
#ensure wifi connected
while(fail_count<4):
    s = os.popen("iwconfig").read()
    if 'Not-Associated' in s:
        fail_count += 1
        s = os.popen("iwconfig wlan0 essid NJU-WLAN").read()
        time.sleep(1.5)
        #s = os.popen("ifconfig wlan0 up").read()
    else:
        fail_count = 0
        break
if(fail_count>=4):
    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('failed @ boot connecting wifi\n')
    f.close()
    time.sleep(2)
    s = os.popen("reboot")
#ensure gain ip
while(fail_count<=3):
    s = os.popen("ifconfig").read()
    if '172' in s:
        fail_count = 0
        break
    else:
        fail_count += 1
        s = os.popen("dhclient wlan0")
        time.sleep(2)
if(fail_count>=3):
    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('failed @ boot gain ip\n')
    f.close()
    time.sleep(2)
    s = os.popen("reboot")

#ensure connect vpn:
while(fail_count<=3):
    s = os.popen("pon shinez").read()
    time.sleep(6)
    s = os.popen("ifconfig").read()
    if 'ppp0' in s:
        fail_count = 0
        break
    else:
        fail_count += 1
if(fail_count>=3):
    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('failed @ boot connect vpn\n')
    f.close()
    time.sleep(2)
    s = os.popen("reboot")
os.popen("ifconfig > /home/pi/rpi_sniff2.0/if_boot_log.txt")
#set route
s = os.popen("ip route del default").read()
while(fail_count<=3):
    s = os.popen("ip route add default dev ppp0").read()
    s = os.popen("ip route").read()
    if 'default' in s:
        print s
        fail_count = 0
        break
    else:
        fail_count += 1

if(fail_count>=3):
    time.sleep(2)
    reboot

s = os.popen("resolvconf -d wlan0").read()
s = os.popen("resolvconf -a ppp0 < /home/pi/vpn_dns").read()
s = os.popen("/etc/init.d/ntp stop").read()
s = os.popen("ntpdate -u time.windows.com").read()

f = open('/home/pi/rpi_sniff2.0/log.txt','a')
f.write('got time\n')
f.close()
while(1):
    stop = open('/home/pi/rpi_sniff2.0/stop.txt');
    line = stop.readline()
    if '1' in line:
        break
    stop.close()
    s = os.popen("ifconfig").read()
    if 'ppp0' in s:
        s = os.popen("poff shinez")
    if '172' in s:
        s = os.popen("dhclient wlan0 -r")
    s = os.popen("ifconfig wlan0 down").read()
    #ensure wlan0 Monitor
    while(fail_count<=3):
        s = os.popen("iwconfig wlan0 mode monitor").read()
        res = os.popen("iwconfig").read()
        if 'Monitor' in res:
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write('fail @ monitor mode\n')
        f.close()
        
        time.sleep(2)
        s = os.popen("reboot")
    s = os.popen("ifconfig wlan0 up").read()
    #start sniff
    subprocess.call("/usr/bin/python /home/pi/rpi_sniff2.0/gather.py",shell = True)

    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('gathered\n')
    f.close()

    s = os.popen("ifconfig wlan0 down")
    #ensure wlan0 Managed
    while(fail_count<=3):
        s = os.popen("iwconfig wlan0 mode managed").read()
        time.sleep(1)
        res = os.popen("iwconfig").read()
        if 'Managed' in res:
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write('failed @ switch to managed mode\n')
        f.close()

        time.sleep(2)
        os.popen("reboot")
    #s = os.popen("/etc/init.d/networking restart").read()
    s = os.popen("iwconfig wlan0 essid NJU-WLAN").read()
    s = os.popen("ifconfig wlan0 up").read()
    time.sleep(2)
    #ensure wifi connected
    while(fail_count<=3):
        s = os.popen("iwconfig").read()
        if 'Not-Associated' in s:
            fail_count += 1
            s = os.popen("iwconfig wlan0 essid NJU-WLAN").read()
            time.sleep(2)
            #s = os.popen("ifconfig wlan0 up").read()
        else:
            os.popen("iwconfig > /home/pi/rpi_sniff2.0/iw_log.txt")
            fail_count = 0
            break
    if(fail_count>=3):
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write('failed @ connecting wifi\n')
        f.close()
        time.sleep(2)
        s = os.popen("reboot")

    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f,write('is going to dhclient')
    f.close()

    with open('/home/pi/rpi_sniff2.0/log.txt') as log:
        log.write('dhclient wlan0 -r\n')
    s = os.popen("dhclient wlan0 -r").read()
    s = os.popen("dhclient wlan0").read()
    with open('/home/pi/rpi_sniff2.0/log.txt') as log:
        log.write('dhcliented wlan0\n')
    #ensure gain ip
    while(fail_count<=3):
        s = os.popen("ifconfig").read()
        if '172' in s:
            os.popen("ifconfig > /home/pi/rpi_sniff2.0/if_log.txt")
            fail_count = 0
            break
        else:
            fail_count += 1
            with open('/home/pi/rpi_sniff2.0/log.txt') as log:
                log.write('dhclient wlan0 -r\n')
            s = os.popen("dhclient wlan0 -r").read()
            s = os.popen("dhclient wlan0").read()
            with open('/home/pi/rpi_sniff2.0/log.txt') as log:
                log.write('dhcliented wlan0\n')
            time.sleep(1)
    if(fail_count>=3):
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write('failed @ gain ip\n')
        f.close()
        time.sleep(2)
        s = os.popen("reboot")

    #DNS
    #s = os.popen("ip route add 114.212.0.0/16 dev wlan0")
    #time.sleep(0.5)

    #set wlan0 route
    s = os.popen("ip route del default").read()
    while(fail_count<=3):
        s = os.popen("ip route add default dev wlan0").read()
        s = os.popen("ip route add 172.26.20.197 dev wlan0").read()
        s = os.popen("ip route").read()
        if 'default' in s:
            print s
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write('failed @ set route wlan0\n')
        f.close()
        time.sleep(2)
        s = os.popen("reboot")

    #ensure being able to ping server
    while(fail_count<=6):
        s = os.popen("ping 172.26.20.197 -c 2").read()
        if "time=" in s:
            f = open('/home/pi/rpi_sniff2.0/log.txt','a')
            f.write('ping server ok\n')
            f.close()
            fail_count = 0
            break
        else:
            fail_count += 1
            f = open('/home/pi/rpi_sniff2.0/log.txt','a')
            f.write('ping failed \n')
            f.close()
            time.sleep(2)
    if fail_count>=6 :
        os.popen("ifconfig > /home/pi/rpi_sniff2.0/if_log.txt")
        os.popen("ip route > /home/pi/rpi_sniff2.0/route_log.txt")
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write("can not ping server\n")
        f.close()
        time.sleep(2)
        os.popen("reboot")

    #ensure connect vpn:
    while(fail_count<=3):
        s = os.popen("pon shinez").read()
        time.sleep(6)
        s = os.popen("ifconfig").read()
        if 'ppp0' in s:
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write('failed @ connect vpn\n')
        f.close()
        
        time.sleep(2)
        os.popen("reboot")
    #set route vpn
    s = os.popen("ip route del default")
    time.sleep(3)
    while(fail_count<=3):
        s = os.popen("ip route add default dev ppp0").read()
        time.sleep(1.5)
        s = os.popen("ip route").read()
        if 'default' in s:
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        f = open('/home/pi/rpi_sniff2.0/log.txt','a')
        f.write('failed @ set route vpn\n')
        f.close()
        time.sleep(2)
        s = os.popen("reboot")
    
    s = os.popen("resolvconf -d wlan0")
    s = os.popen("resolvconf -a ppp0 < /home/pi/vpn_dns")
    #send
    #s = subprocess.call("/usr/bin/python /home/pi/rpi_sniff2.0/send_mail.py",shell = True)
    time.sleep(2)
    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('is going to upload\n')
    f.close()
    s = subprocess.call("/usr/bin/python /home/pi/rpi_sniff2.0/upload.py",shell = True)

    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('sent\n')
    f.close()
    time.sleep(1)

