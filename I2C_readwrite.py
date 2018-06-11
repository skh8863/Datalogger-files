"""
This program tests the functionality of an I2C connection with the Kionix KX022
accelerometer. The registers are set in the first block of code, and raw data
output from each of the axes is recorded into a list for 1 second. After this
interval the data from each list is written to a file. Loops infinitely until
a keyboard interrupt is issued by the user. Block of code which is commented
out deals with taking data from the buffer of the sensor, which was unreliable
when first tested.

"""

import os
import datetime
import csv

import smbus
DEVICE_BUS = 1
DEVICE_ADDR = 0x1F
bus = smbus.SMBus(DEVICE_BUS)

"""
I2C Addresses:

CNTL1: 0x18
ODCNTL: 0x1B
BUF_CNTL2: 0x3B
Z_OUT_H: 0x0B
BUF_READ: 0x3F
XOUT_L: 0x06
XOUT_H: 0x07
YOUT_L: 0x08
YOUT_H: 0x09
ZOUT_L: 0x0A
ZOUT_H: 0x0B

"""

bus.write_byte_data(DEVICE_ADDR, 0x18, 0x48)
bus.write_byte_data(DEVICE_ADDR, 0x1B, 0xC7)
bus.write_byte_data(DEVICE_ADDR, 0x3B, 0xC0)
bus.write_byte_data(DEVICE_ADDR, 0x18, 0xC8)
#bus.write_byte_data(DEVICE_ADDR, 0x3A, 6)    #sets sample threshold of buffer

#x_low = []
#x_high = []
#y_low = []
#y_high = []
#z_low = []
#z_high = []

#print(bus.read_byte_data(DEVICE_ADDR, 0x13))    #reads register which tells which function caused interrupt

#bus.write_byte_data(DEVICE_ADDR, 0x3E, 0xFF)   #clears buffer
#time.sleep(1)
#bus.write_byte_data(DEVICE_ADDR, 0x3B, 0x40)    #disables buffer

#for i in range(12):
   #value = bus.read_byte_data(0x1F, 0x3F)    #reads from buffer

#    if i == 0 or i%6 == 0:
#        x_low.append(value)
#    elif (i-1)%6 == 0:
#        x_high.append(value)
#    elif (i-2)%6 == 0:
#        y_low.append(value)
#    elif (i-3)%6 == 0:
#        y_high.append(value)
#    elif (i-4)%6 == 0:
#        z_low.append(value)
#    elif (i-5)%6 == 0:
#        z_high.append(value)

xdata = []
ydata = []
zdata = []

try:
    os.remove('test.csv')
except OSError:
    pass

t1 = datetime.datetime.now()
try:
    while True:
        x_low = bus.read_byte_data(0x1F, 0x06)
        x_high = bus.read_byte_data(0x1F, 0x07)
        x = hex(int((format(x_high, '08b')+format(x_low, '08b')), 2))
        xdata.append(x)

        y_low = bus.read_byte_data(0x1F, 0x08)
        y_high = bus.read_byte_data(0x1F, 0x09)
        y = hex(int((format(y_high, '08b')+format(y_low, '08b')), 2))
        ydata.append(y)

        z_low = bus.read_byte_data(0x1F, 0x0A)
        z_high = bus.read_byte_data(0x1F, 0x0B)
        z = hex(int((format(z_high, '08b')+format(z_low, '08b')), 2))
        zdata.append(z)

        t2 = datetime.datetime.now()

        if (t2-t1).seconds > 1:
            print('I got here')
            with open('test.csv', 'w+') as f:
                writer = csv.writer(f)
                writer.writerow(xdata)
                writer.writerow(ydata)
                writer.writerow(zdata)
                xdata = []
                ydata = []
                zdata = []
                f.close()
                t1 = datetime.datetime.now()
except KeyboardInterrupt:
    print("terminated")

#print(x_low, x_high, y_low, y_high, z_low, z_high)

#print(bus.read_byte_data(DEVICE_ADDR, 0x13))    #reads register which tells which function caused interrupt
#bus.write_byte_data(DEVICE_ADDR, 0x3E, 0xFF)    #clears buffer
