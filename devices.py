'''define device class'''

class device:
    def __init__(self,stre,ldtime,rtime,mac):
        self.strength = stre
        self.last_ditected_time = ldtime
        self.real_time = rtime
        self.mac_addr = mac

    def update(self,stre,ldtime,rtime):
        self.strength = stre
        self.last_ditected_time = ldtime
        self.real_time = rtime

    def myprint(self):
        return self.mac_addr+' '+str(self.strength)+' '+str(self.real_time)

''' TEST '''
def main():
    d0 = device(-45,2015,'qwer')
    print d0.last_ditected_time,d0.mac_addr,d0.strength
    d0.update(-35,2014)
    print d0.last_ditected_time,d0.mac_addr,d0.strength


if __name__ == '__main__':
    main()
