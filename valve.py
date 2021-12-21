#from datetime import datetime
import time, sys
import pigpio
from hwpwm import set_voltage
from enum import Enum

def mock_set_voltage(pi, val):
    print("----- MOCK: Setting voltage to {} V. -----".format(val))

class State(Enum):
    CLOSED = 0
    OPENING = 1
    OPEN = 2
    CLOSING = 3

class Valve:
    def __init__(self, openTime=120, openVoltage=7.0, maintainVoltage=2.0):
        self.openTime = openTime
        self.ov = openVoltage
        self.mv = maintainVoltage
        self.openingTime = 1.5
        self.state = State.CLOSED
        self.pi = pigpio.pi()
        self.timer = 0
        set_voltage(self.pi, 0)
    
    def open(self, openTime):
        self.openTime = openTime
        set_voltage(self.pi, self.ov)
        self.timer = time.time()
        self.state = State.OPENING
        time.sleep(self.openingTime)
        set_voltage(self.pi, self.mv)
        self.state = State.OPEN

    def keep_open(self, t):
        self.openTime = t
        if self.state == State.OPEN or self.state == State.OPENING:
            self.timer = time.time()
        else:
            self.open(openTime=t)
        self.status()

    def close(self):
        set_voltage(self.pi, 0.0)
        self.state = State.CLOSING
        time.sleep(1.0)
        self.state = State.CLOSED

    def auto_close(self):
        while(self.state != State.CLOSED):
            self.status()
            if time.time() > (self.timer + self.openTime):
                print("Timer expired, closing valve")
                self.close()
                self.status()
            time.sleep(0.5)
            sys.stdout.flush()

    def status(self):
        print("Valve state: {}".format(self.state))
        elapsedTime = time.time() - self.timer
        remainingTime = self.openTime - elapsedTime 
        if self.state == State.OPEN:
            print("Valve closing in {} seconds".format(remainingTime))

        sys.stdout.flush()

import threading

def statusPoll():
    print("Gurka")
    global v
    v.auto_close()

def main():
    global v 
    v = Valve(openTime=10, openVoltage=7.0, maintainVoltage=2.0)
    

    thr = threading.Thread(target=statusPoll)
    thr.daemon = True
    #thr.start()


    print("start: {}".format(time.time()))
    v.status()
    v.open(10)
    thr.start()
    #v.status()
    print("sleep 5")
    time.sleep(5.0)
    #v.status()
    print("keep 11")
    v.keep_open(11)
    #v.status()
    thr.join()
    time.sleep(12)


if __name__ == '__main__':
    main()
