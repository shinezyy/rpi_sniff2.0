# post to server

import urllib
import urllib2
import json

PC_test = True


def upload_post(data_dict):
    try:
        url = 'http://3.raspberrypiserver.sinaapp.com/trainer/pi/'
        # url = 'http://192.168.1.117:8000/update/'
        data_str = urllib.urlencode(data_dict)
        req = urllib2.Request(url,data_str)
        response = urllib2.urlopen(req)
        # print response
    except :
        with open('/home/pi/rpi_sniff2.0/log.txt','a') as f:
            f.write('failed to upload')


def main():
    if PC_test:
        json_file = 'data.json'
    else:
        json_file = '/home/pi/rpi_sniff2.0/data.json'
    with open(json_file,'r') as f:
        data = json.load(f)
    for data_dict in data:
        print data_dict
        # upload_post(data_dict)


if __name__ == '__main__':
    main()
