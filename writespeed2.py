"""
A second version of writespeed.py. This was created in an attempt to eliminate
any repetition by using a for loop to iterate over the different number of
factors of 2 instead of writing out the same code three times.

"""

import os
import datetime
import numpy as np
import csv

list10 = []
list100 = []
list1000 = []

for j in range(100):
    
    datalist = []
    try:
        os.remove('test.csv')
    except OSError:
        pass

    for k in range(3):
        for i in range(10**(k+1)):
            x = 2*i
            datalist.append(x)

        start = datetime.datetime.now()

        with open('test.csv', 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(datalist)

        f.close()

        end = datetime.datetime.now()
        diff = (end-start)

        if k == 0:
            list10.append(diff.microseconds)
        elif k == 1:
            list100.append(diff.microseconds)
        elif k == 2:
            list1000.append(diff.microseconds)

meantime10 = np.mean(list10)
meantime10 = meantime10/1000
meantime100 = np.mean(list100)
meantime100 = meantime100/1000
meantime1000 = np.mean(list1000)
meantime1000 = meantime1000/1000
print(str(meantime10)+' ms')
print(str(meantime100)+' ms')
print(str(meantime1000)+' ms')