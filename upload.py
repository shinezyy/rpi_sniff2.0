# post to server

import urllib
import urllib2
import json
from config import *


def upload_post(data_dict):
    if PC_test:
        work_dir = './'
    else:
        work_dir = '/home/pi/rpi_sniff2.0/'

    try:
        url = 'http://' + server_ip_addr + '/trainer/pi/'
        data_str = urllib.urlencode(data_dict)
        req = urllib2.Request(url,data_str)
        response = urllib2.urlopen(req)
        # print response
        return True, ''
    except :
        return False, 'failed to upload'



def upload():
    if PC_test:
        work_dir = './'
    else:
        work_dir = '/home/pi/rpi_sniff2.0/'

    json_file = work_dir + 'data.json'

    with open(json_file,'r') as f:
        data = json.load(f)
    for data_dict in data:
        print 'Is uploading', data_dict
        if send_to_server:
            ret = upload_post(data_dict)
    return True, ''

