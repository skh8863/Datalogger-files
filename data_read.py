"""
This program reads the data written by either SPI_readwrite or I2C_readwrite
and converts the hex data into acceleration values. Acceleration range of the
accelerometer can be specified through user input, and conversion is adjusted
accordingly.

"""

import csv

with open('test.csv', 'rb') as f:
    reader = csv.reader(f)
    datalist = list(reader)

f.close()

x = datalist[0]
y = datalist[1]
z = datalist[2]

x_int = []
y_int = []
z_int = []

x_accel = []
y_accel = []
z_accel = []

for i in range(len(x)):
    x_int.append(int(x[i],0))
    y_int.append(int(y[i],0))
    z_int.append(int(z[i],0))

print(min(x_int), max(x_int))
print(min(y_int), max(y_int))
print(min(z_int), max(z_int))

range = input('Acceleration range in g? (Enter 2,4,8): ')

def accel_convert(list, accel_list):
    for data in list:
        val = float(32767-data)
        conversion = float(-range)/float(32768)
        if data < 0:
            accel_list.append(val*conversion)
        if data > 0:
            accel_list.append(val*conversion)
        if data == 0:
            accel_list.append(0)

accel_convert(x_int, x_accel)
accel_convert(y_int, y_accel)
accel_convert(z_int, z_accel)

print(format(min(x_accel), '.5g'), format(max(x_accel), '.5g'))
print(format(min(y_accel), '.5g'), format(max(y_accel), '.5g'))
print(format(min(z_accel), '.5g'), format(max(z_accel), '.5g'))
