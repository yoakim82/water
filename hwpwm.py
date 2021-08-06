import pigpio
import time
PWMPIN = 12
PWMFREQ = 38000
DUTYMAX = 1000000


duty = 0.5


pi = pigpio.pi()
 
def status(v, v2=None):
    if v2 != None:
        print("exact value: {}".format(v2))
    
    print("setting voltage to {} V".format(v))

def set_voltage(pi, v):
    PWMPIN = 12
    PWMFREQ = 38000
    DUTYMAX = 1000000
    MAX_VOLT = 12.0    
    duty = float(v)/MAX_VOLT
    duty_value = int(duty * DUTYMAX)
    status(v, duty)
    print(duty_value)
    pi.hardware_PWM(PWMPIN, PWMFREQ, duty_value)


#for v in range(0, 5):
    #status(v)
#    set_voltage(pi, v)
#    time.sleep(2.5)

#for v in range (5,-1,-1):
    #status(v)
#    set_voltage(pi, v)
#    time.sleep(2.5)

#set_voltage(pi, 5)
#time.sleep(1.5)
#set_voltage(pi, 2)
#time.sleep(1.0)

#set_voltage(pi, 7)
#time.sleep(1.0)
#set_voltage(pi, 2)
#time.sleep(10.0)
set_voltage(pi, 0)



