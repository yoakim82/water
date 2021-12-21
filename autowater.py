import pdb
from datetime import datetime
import time,sys
from valve import State,Valve

debug = False
rxMess = None
newMess = False


#v = Valve(openTime=10, openVoltage=7.0, maintainVoltage=2.0)


class Values():
    def __init__(self, n=50):
        self.v = []
        self.maxLen = n

    def _push(self, value):
        self.v.append(value)

    def _pop(self, value):
        ret = self.v[0]
        self.v = self.v[1:]
        return ret

    def shift(self, v):
        self._push(v)
        self._pop()

    def add(self, v):
        self._push(v)
        if len(self.v) > self.maxLen:
            self._pop(v)

    def avg(self):
        if len(self.v) > 0:
            return float(sum(self.v)/len(self.v))
        else:
            return 0.0

class Chirp():
    def __init__(self):
        self.v = 3.0

    def measure(self):
        return self.v

    def set(self, val): 
        self.v = val


#CLEAN_SESSION=False
def main():

    valve = Valve(openTime=10, openVoltage=7.0, maintainVoltage=2.0)
    moist = Values(n=20)
    sensor = Chirp()
    sensor.set(20.0)
    interval = 10
    thres = 30.0
    timeToWater = interval
    openTime = 5
    while True:

        moist.add(sensor.measure())
        print("Time to Water: {}".format(timeToWater))
        if timeToWater == 0:
            print("avg: {}".format(moist.avg()))
            if moist.avg() < thres:
                print("watering")
                valve.keep_open(openTime)
                valve.auto_close()
            else:
                print("Nope, too wet")

            timeToWater = interval
        
        timeToWater = timeToWater - 1
        time.sleep(1.0)


if __name__ == '__main__':
    main()
