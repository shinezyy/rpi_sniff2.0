#!/usr/bin/python

import os
import subprocess
import time
from subprocess import check_output
from config import *
from upload import upload
from upload import connected
from pitime import syn_time
from time import gmtime, strftime

time_before_reboot = 30

init()


if PC_test:
    work_dir = './'
else:
    work_dir = '/home/pi/rpi_sniff2.0/'

log_file = 'log.txt'
error_dump_file = 'error.txt'
stop_file = 'stop.txt'
fault_level = 'no fault'
wifi_waiting_interval = 5


def try_many_times(func, times, handle=None):
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
        elif handle:
            handle()
    if not suc:
        with open(work_dir+error_dump_file, 'w') as edf:
            print >> edf, error_msg
        return False


def log_to_file(msg):
    if PC_test:
        print msg
    with open(work_dir+log_file, 'a') as lf:
        lf.write(msg + '-----' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n')


def connect_wifi():
    ret = check_output(['iwconfig'])
    if 'Not-Associated' not in ret:
        return True, ''
    # not connected yet
    not_used = check_output(("iwconfig wlan0 essid "+WLAN_SSID).split())
    time.sleep(wifi_waiting_interval)
    ret = check_output(['iwconfig'])
    if 'Not-Associated' not in ret:
        return True, ''
    else:
        return False, 'Failed to connect NJU WLAN'


def get_ip():
    ret = check_output("ifconfig")
    if ip_start in ret:
        if connected():
            return True, ''
        else:
            log_to_file("Not connected to server, release IP")
            not_used = check_output("dhclient wlan0 -r".split())
    # not got yet
    not_used = check_output("dhclient wlan0".split())

    log_to_file('Finished dhclient')
    ret = check_output("ifconfig")
    if ip_start in ret and connected():
            return True, ''
    elif ip_start in ret and not connected():
        log_to_file('Got IP but cannot connect to server.')
        return False, 'Got IP but cannot connect to server.'
    else:
        log_to_file('Cannot get IP')
        return False, 'Cannot get IP'


def stop():
    global work_dir, stop_file
    with open(work_dir + stop_file) as sf:
        first_line = sf.readline()
        if '1' in first_line:
            return True
        else:
            return False


def release_ip():
    s = check_output(['ifconfig'])
    if ip_start in s:
        not_used = check_output("dhclient wlan0 -r".split())


def turn_down_wireless_card():
    not_used = check_output("ifconfig wlan1 down".split())


def turn_on_wireless_card():
    not_used = check_output("ifconfig wlan1 up".split())


def switch_monitor_mode():
    ret1 = check_output("iwconfig wlan1 mode monitor".split())
    ret2 = check_output(["iwconfig"])
    if 'Monitor' in ret2:
        return True, ''
    else:
        return False, 'Failed to switch to monitor mode'


def switch_managed_mode():
    not_used = check_output("iwconfig wlan1 mode managed".split())
    ret2 = check_output("iwconfig".split())
    if 'Managed' in ret2:
        return True, ''
    else:
        return False, 'Failed to switch to Managed mode'


def network_restart():
    not_used = check_output("/etc/init.d/networking restart".split())


def reboot():
    if PC_test:
        log_to_file('Stop because of too many errors!')
        return
    log_to_file('Is going to reboot')
    time.sleep(time_before_reboot)
    subprocess.Popen('reboot', shell=True)


def try_with_restart(func, times, handle=None):
    if not try_many_times(func, times):
        network_restart()
        if handle:
            handle()
        if not try_many_times(func, times):
            reboot()

# get time


def main():
    turn_down_wireless_card()
    try_with_restart(switch_monitor_mode, 3)
    turn_on_wireless_card()

    # connect wifi
    try_with_restart(connect_wifi, 5)
    # get ip
    try_with_restart(get_ip, 5)
    # get time
    try_with_restart(syn_time, 5)

    while True:
        if stop():
            break

        # start sniff
        check_output(['/usr/bin/python', work_dir+'gather.py'])
        log_to_file('Gathered mac addresses')

        # send to server
        time.sleep(1)
        if connected():
            log_to_file('Network is OK, and is going to upload!')
            try_with_restart(upload, 3, connect_wifi)
        else:
            try_with_restart(get_ip, 5)


if __name__ == '__main__':
    main()

