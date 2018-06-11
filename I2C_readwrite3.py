"""
Slight modification of I2C_readwrite2.py, using interrupts to ensure sensor is
not being overrun, and only new data is written to a list and subsequently
written to a file. Used as a diagnostic for I2C speeds and number of data
points which can be written per second; useful in determining optimal output
data rate.
"""
import os
import datetime
import numpy as np
import csv
import time
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
INS2: 0x13
XOUT_L: 0x06
XOUT_H: 0x07
YOUT_L: 0x08
YOUT_H: 0x09
ZOUT_L: 0x0A
ZOUT_H: 0x0B
"""

bus.write_byte_data(DEVICE_ADDR, 0x18, 0x68)
bus.write_byte_data(DEVICE_ADDR, 0x1B, 0xC7)
bus.write_byte_data(DEVICE_ADDR, 0x3B, 0xC0)
#bus.write_byte_data(DEVICE_ADDR, 0x35, 0x0B)
bus.write_byte_data(DEVICE_ADDR, 0x18, 0xE8)

xdata = []
ydata = []
zdata = []

time_list = []
num_xdata = []

data_interval = 0.5

for i in range(10):
    try:
        os.remove('test.csv')
    except OSError:
        pass

    t2 = time.time() + data_interval

    while time.time() < t2:
        val = bus.read_byte_data(0x1F, 0x13)
        bit = (val&0x10)>>4
        if bit == 1:
            x_low = bus.read_byte_data(0x1F, 0x06)
            x_high = bus.read_byte_data(0x1F, 0x07)
            x = hex(int((format(x_high, '08b')+format(x_low, '08b')), 2))
            xdata.append(x)
            num_xdata.append(len(xdata))

            y_low = bus.read_byte_data(0x1F, 0x08)
            y_high = bus.read_byte_data(0x1F, 0x09)
            y = hex(int((format(y_high, '08b')+format(y_low, '08b')), 2))
            ydata.append(y)

            z_low = bus.read_byte_data(0x1F, 0x0A)
            z_high = bus.read_byte_data(0x1F, 0x0B)
            z = hex(int((format(z_high, '08b')+format(z_low, '08b')), 2))
            zdata.append(z)
        else:
            pass

    t3 = datetime.datetime.now()
    with open('test.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(xdata)
        writer.writerow(ydata)
        writer.writerow(zdata)
        xdata = []
        ydata = []
        zdata = []
        f.close()
    t4 = datetime.datetime.now()
    time_list.append((t4-t3).microseconds)

print('Average time spent per open-write-close operation: '+str(np.mean(time_list)/1000)+' ms')
print('Average data points per sec: '+str(np.mean(num_xdata)/data_interval))
