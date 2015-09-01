'''post to server'''

import urllib
import urllib2
import json

def upload_post(data_dict):
    #url = 'http://raspberrypiserver.sinaapp.com/update/'
    url = 'http://192.168.1.117:8000/update/'
    data_str = urllib.urlencode(data_dict)
    req = urllib2.Request(url,data_str)
    response = urllib2.urlopen(req)

def main():
    with open('data.json','r') as f:
        data = json.load(f)
    print data
if __name__ == '__main__':
    main()
