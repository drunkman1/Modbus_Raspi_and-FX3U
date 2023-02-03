import minimalmodbus
import time
#import serial
import RPi.GPIO as GPIO
#minimalmodbus.get_diagnostic_string()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
#GPIO.setup(14, GPIO.OUT)
GPIO.output(4,GPIO.HIGH)
#GPIO.output(14, GPIO.LOW)

time.sleep(1)

fx3u = minimalmodbus.Instrument('/dev/ttyAMA0', 1)
fx3u.mode = minimalmodbus.MODE_RTU
fx3u.debug = False
fx3u.serial.baudrate = 9600
#fx3u.serial.parity = serial.PARITY_NONE
fx3u.serial.bytesize = 8
fx3u.serial.stopbits = 1
fx3u.serial.timeout = 2
fx3u.serial.write_timeout = 1
#fx3u.address = 0
#fx3u.handle_local_echo = True
fx3u.write_bit(1,0,functioncode=5)
#fx3u.write_register(1,2,functioncode= 16)
print('1')
GPIO.output(4, GPIO.LOW)

GPIO.cleanup()