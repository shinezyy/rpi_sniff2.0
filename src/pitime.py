import time
import urllib
import urllib2
import os

from config import c

ISO_TIME_FORMAT = '%Y-%m-%d %X'
MINUTE_TIME_FORMAT = '%X'


def get_current_time():
    return time.strftime(ISO_TIME_FORMAT,time.localtime())


def get_current_minute():
    return time.time()


def get_current_time():
    not_used1 = os.popen("/etc/init.d/ntp stop").read()
    ntp_msg = os.popen("ntpdate -u ntp.nju.edu.cn").read()


def syn_time():
    url = 'http://' + c.server_ip_addr + '/syn/'
    req = urllib2.Request(url)
    cmd = urllib2.urlopen(req).read()
    print cmd
    cmd1, cmd2, cmd3, nouse = cmd.split('\n')
    r = os.popen(cmd1).read()
    r = os.popen(cmd2).read()
    r = os.popen(cmd3).read()

    return True, ''

