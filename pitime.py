import time

ISO_TIME_FORMAT = '%Y-%m-%d %X'
MINUTE_TIME_FORMAT = '%X'


def get_current_time():
    return time.strftime(ISO_TIME_FORMAT,time.localtime())


def get_current_minute():
    return time.time()


def get_current_time():
    not_used1 = os.popen("/etc/init.d/ntp stop").read()
    ntp_msg = os.popen("ntpdate -u ntp.nju.edu.cn").read()
    log_to_file('ntp msg:\n'+ntp_msg+'\n')

