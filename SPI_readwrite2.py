"""
Consolidated version of SPI_readwrite.py, utilizing functions to reduce
repetitions in code. Also have eliminated checking of whether output file
exists, since deletion of the file was simply for diagnostics. This program
functions more as a usable data-logging program.

"""

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

spi.xfer2([0x18, 0x60])
spi.xfer2([0x1B, 0xC7])
spi.xfer2([0x18, 0xE0])

xdata = []
ydata = []
zdata = []

time_list = []
num_xdata = []

data_interval = 1

def read_register(reg_address):
    address = 0x80 | reg_address
    value = spi.xfer2([address, 0x00])
    return value[1]

for i in range(10):

    t2 = time.time() + data_interval

    while time.time() < t2:
        val = read_register(0x13)
        bit = (val&0x10)>>4
        if bit == 1:
            x_low = read_register(0x06)
            x_high = read_register(0x07)
            x = hex(int((format(x_high, '08b')+format(x_low, '08b')), 2))
            xdata.append(x)
            num_xdata.append(len(xdata))

            y_low = read_register(0x08)
            y_high = read_register(0x09)
            y = hex(int((format(y_high, '08b')+format(y_low, '08b')), 2))
            ydata.append(y)

            z_low = read_register(0x0A)
            z_high = read_register(0x0B)
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
