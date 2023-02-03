""" import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG) """

import time
import serial
import RPi.GPIO as GPIO
from time import sleep

from pymodbus.client.sync import ModbusSerialClient
#import minimalmodbus
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.output(4,1)
GPIO.output(18,GPIO.HIGH)
GPIO.setup(8, GPIO.OUT)
GPIO.output(18,GPIO.HIGH)
time.sleep(1)

fx3u = ModbusSerialClient(method='rtu'
                        , port='/dev/ttyAMA0'
                        , baudrate= 9600
                        , parity='N'
                        , stopbits= 1
                        , bytesie = 8
                        , timeout=0.05
                        )


fx3u.connect()

#print(fx3u.is_socket_open())
a = [0,0,0,0,0,0,0,0,0,9]
a[0] = 1
fx3u.write_registers(0,a,unit=1)
fx3u.write_coil(0,1,unit=1)
fx3u.write_coil(1,1,unit=1)

rd = fx3u.read_holding_registers(0,1,unit=1)
print(rd)

#
#fx3u.write_register(0,1,unit=1)


#print(fx3u.read_input_registers(1,10,unit=1))
""" for i in range(10):
    fx3u.write_coil(1,1,unit=1)
    #time.sleep(0.05)
    fx3u.write_coil(1,0,unit=1)
    #time.sleep(0.05)
    print(i) """
fx3u.close()
GPIO.output(4, GPIO.LOW)
