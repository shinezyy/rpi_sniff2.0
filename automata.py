#!/usr/bin/python

import os
import subprocess
import time

time_before_reboot = 30

PC_test = True

if PC_test:
    work_dir = './'
else:
    work_dir = '/home/pi/rpi_sniff2.0/'

log_file = 'log.txt'
error_dump_file = 'error.txt'
stop_file = 'stop.txt'


def try_many_times(func, times):
    # func: return bool, string
    # bool to indicate whether successfully done
    # string to Error dump

    assert times > 0
    suc = False
    error_msg = 'Not tried !'
    for i in range(0, times):
        suc, error_msg = func()
        if suc:
            return True
    if not suc:
        with open(error_dump_file, 'w') as edf:
            print >> edf, error_msg
        return False


def log_to_file(msg):
    with open(work_dir+log_file, 'a') as lf:
        lf.write(msg + '\n')


def connected_wifi():
    ret = os.popen("iwconfig").read()
    if 'Not-Associated' not in ret:
        return True, ''
    # not connected yet
    ret = os.popen("iwconfig wlan0 essid NJU-WLAN").read()
    if 'Not-Associated' not in ret:
        return True, ''
    else:
        return False, 'Failed to connect NJU WLAN'


def got_ip():
    ret = os.popen("ifconfig").read()
    if '172' in ret:
        return True, ''
    # not got yet
    ret = os.popen("dhclient wlan0")
    if '172' in ret:
        return True, ''
    else:
        return False, 'Failed to got ip from NJU WLAN'


def get_current_time():
    not_used1 = os.popen("/etc/init.d/ntp stop").read()
    ntp_msg = os.popen("ntpdate -u time.windows.com").read()
    log_to_file('ntp msg:\n'+ntp_msg+'\n')


def stop():
    global work_dir, stop_file
    with open(work_dir + stop_file) as sf:
        first_line = sf.readline()
        if '1' in first_line:
            return True
        else:
            return False


def release_ip():
    s = os.popen("ifconfig").read()
    if '172' in s:
        os.popen("dhclient wlan0 -r")


def turn_down_wireless_card():
    not_used = os.popen("ifconfig wlan0 down").read()


def turn_on_wireless_card():
    not_used = os.popen("ifconfig wlan0 up").read()


def switch_monitor_mode():
    ret1 = os.popen("iwconfig wlan0 mode monitor").read()
    ret2 = os.popen("iwconfig").read()
    if 'Monitor' in ret2:
        return True, ''
    else:
        return False, 'Failed to switch to monitor mode'


def switch_managed_mode():
    ret1 = os.popen("iwconfig wlan0 mode managed").read()
    ret2 = os.popen("iwconfig").read()
    if 'Managed' in ret2:
        return True, ''
    else:
        return False, 'Failed to switch to Managed mode'


while True:
    if stop():
        break
    release_ip()

    turn_down_wireless_card()
    # switch to Monitor mode
    turn_on_wireless_card()

    # start sniff
    subprocess.call('/usr/bin/python'+work_dir+'gather.py', shell=True)
    log_to_file('Gathered mac addresses')

    turn_down_wireless_card()
    # switch to Managed mode
    turn_on_wireless_card()

    #s = os.popen("/etc/init.d/networking restart").read()
    s = os.popen("iwconfig wlan0 essid NJU-WLAN").read()
    s = os.popen("ifconfig wlan0 up").read()

    # connect wifi

    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('is going to dhclient\n')
    f.close()

    s = os.popen("dhclient wlan0 -r").read()

    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('finished  dhclient -r\n')
    f.close()

    s = os.popen("dhclient wlan0").read()

    f = open('/home/pi/rpi_sniff2.0/log.txt','a')
    f.write('finished  dhclient wlan0\n')
    f.close()

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
        time.sleep(time_before_reboot)
        s = os.popen("reboot")

    #DNS
    #s = os.popen("ip route add 114.212.0.0/16 dev wlan0")
    #time.sleep(0.5)

    '''
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
        time.sleep(time2reboot)
        s = os.popen("reboot")
    '''

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
        time.sleep(time_before_reboot)
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
        
        time.sleep(time_before_reboot)
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
        time.sleep(time_before_reboot)
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

