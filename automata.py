import os
import time

fail_count = 0
boot = 1

while(1):
    if(not boot):
        s = os.popen("poff shinez")
    boot = 0
    s = os.popen("ifconfig wlan0 down")
    #ensure wlan0 Monitor
    while(fail_count<=3):
        s = os.popen("iwconfig wlan0 mode monitor")
        res = os.popen("iwconfig")
        if 'Monitor' in res:
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        print "failed to switching to monitor mode"
        s = os.popen("reboot")
    s = os.popen("ifconfig wlan0 up")
    #start sniff
    s = os.popen("python ./gather.py")
    time.sleep(2)
    s = os.popen("ifconfig wlan0 down")
    #ensure wlan0 Managed
    while(fail_count<=3):
        s = os.popen("iwconfig wlan0 mode managed")
        res = os.popen("iwconfig")
        if 'Managed' in res:
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        print "failed to switch to managed mode"
        s = os.popen("reboot")
    s = os.popen("iwconfig wlan0 essid NJU-WLAN")
    time.sleep(1)
    s = os.popen("ifconfig wlan0 up")
    time.sleep(2)
    #ensure wifi connected
    while(fail_count<=3):
        s = os.popen("iwconfig")
        if 'Not-Associated' in s:
            fail_count += 1
            s = os.popen("iwconfig wlan0 essid NJU-WLAN")
            time.sleep(1)
            s = os.popen("ifconfig wlan0 up")
            time.sleep(2)
        else:
            fail_count = 0
            break
    if(fail_count>=3):
        print "failed to connect wifi"
        s = os.popen("reboot")
    #ensure gain ip
    while(fail_count<=3):
        s = os.popen("ifconfig")
        if '172.26' in s:
            fail_count = 0
            break
        else:
            fail_count += 1
            s = os.popen("dhclient wlan0")
            time.sleep(1)
    if(fail_count>=3):
        print "failed to gain ip"
        s = os.popen("reboot")
    #ensure connect vpn:
    while(fail_count<=3):
        s = os.popen("pon shinez")
        time.sleep(2)
        s = os.popen("ifconfig")
        if 'ppp0' in s:
            fail_count = 0
            break
        else:
            fail_count += 1
    if(fail_count>=3):
        print "failed to connect vpn"
        s = os.popen("reboot")
    #send
    s = os.popen("python ./send_mail.py")


    
