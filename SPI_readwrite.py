"""
This program is the same as I2C_readwrite and its associated versions, but now
using SPI to determine whether I2C was bottlenecking data recording rates and
to further explore possible data-writing rates with varying bus rates, as SPI
supports much higher clock rates than I2C.

"""

import os
import datetime
import numpy as np
import csv
import time
import spidev

"""
I2C Addresses:

CNTL1: 0x18, first set to 0x68, then 0xE8
ODCNTL: 0x1B, set to 0xC7
BUF_CNTL2: 0x3B, set to 0xC0
BUF_READ: 0x3F
INS2: 0x13
XOUT_L: 0x06
XOUT_H: 0x07
YOUT_L: 0x08
YOUT_H: 0x09
ZOUT_L: 0x0A
ZOUT_H: 0x0B
"""

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000000
spi.mode = 0b00

spi.xfer2([0x18, 0x68])
spi.xfer2([0x1B, 0xC7])
spi.xfer2([0x18, 0xE8])

xdata = []
ydata = []
zdata = []

time_list = []
num_xdata = []

data_interval = 100

for i in range(1):
    try:
        os.remove('test.csv')
    except OSError:
        pass

    t2 = time.time() + data_interval



    while time.time() < t2:
        val = spi.xfer2([0x93, 0x00])
        bit = (val[1]&0x10)>>4
        if bit == 1:
            x_low = spi.xfer2([0x86, 0x00])
            x_high = spi.xfer2([0x87, 0x00])
            x = hex(int((format(x_high[1], '08b')+format(x_low[1], '08b')), 2))
            xdata.append(x)
            num_xdata.append(len(xdata))

            y_low = spi.xfer2([0x88, 0x00])
            y_high = spi.xfer2([0x89, 0x00])
            y = hex(int((format(y_high[1], '08b')+format(y_low[1], '08b')), 2))
            ydata.append(y)

            z_low = spi.xfer2([0x8A, 0x00])
            z_high = spi.xfer2([0x8B, 0x00])
            z = hex(int((format(z_high[1], '08b')+format(z_low[1], '08b')), 2))
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
