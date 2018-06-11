"""
This program was written as a diagnostic of the Raspberry Pi's file-writing 
speed to determine the rate at which data could be taken from a sensor and
then written to a file. The program first calculates the first 10 factors of 2
and writes them to a file 100 times, then does the same for the first 100
factors and then the first 1000 factors. Each time the factors are calculated
and written to the file, the program deletes the file and creates it again when
writing to it in order to determine the impact on runtime of creating, opening,
and closing a file. The time taken to open, write, and close the file is
appended to a list whose mean is calculated and printed in milliseconds.

"""

import os
import time
import numpy as np

list10 = []
list100 = []
list1000 = []
for j in range(100):
    try:
        os.remove('test.txt')
    except OSError:
        pass

    start = time.time()
    with open("test.txt", 'w+') as f:

	    for i in range(10):
	        x = 2*i
	        x = str(x)
	        f.write(x)
    
	    f.close()
    
	    end = time.time()
	    diff = (end-start)*1000000
	    diff = int(diff)
	    list10.append(diff)

for j in range(100):
    try:
        os.remove('test.txt')
    except OSError:
        pass

    start = time.time()
    with open("test.txt", 'w+') as f:

	    for i in range(100):
	        x = 2*i
	        x = str(x)
	        f.write(x)
    
	    f.close()
    
	    end = time.time()
	    diff = (end-start)*1000000
	    diff = int(diff)
	    list100.append(diff)

for j in range(100):
    try:
        os.remove('test.txt')
    except OSError:
        pass

    start = time.time()
    with open("test.txt", 'w+') as f:

	    for i in range(1000):
	        x = 2*i
	        x = str(x)
	        f.write(x)
    
	    f.close()
    
	    end = time.time()
	    diff = (end-start)*1000000
	    diff = int(diff)
	    list1000.append(diff)
    
print(np.mean(list10))
print(np.mean(list100))
print(np.mean(list1000))
