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
    ret = os.popen('iwconfig').read()
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
    os.popen("ifconfig wlan0 down").read()


def turn_on_wireless_card():
    os.popen("ifconfig wlan0 up").read()


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


def network_restart():
    os.popen("/etc/init.d/networking restart").read()


def reboot():
    time.sleep(time_before_reboot)
    os.popen('reboot')


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

    # connect wifi
    # get ip

    # send to server
    # s = subprocess.call("/usr/bin/python /home/pi/rpi_sniff2.0/send_mail.py",shell = True)

    time.sleep(1)
    log_to_file('Is going to upload')
    subprocess.call('/usr/bin/python' + work_dir + 'upload.py', shell=True)
    log_to_file('Uploaded')

