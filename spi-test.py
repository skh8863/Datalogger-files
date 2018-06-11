"""
Program written to test SPI functionality and syntax.

"""
import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 488000
spi.mode = 0b00

spi.xfer([0x18, 0x68])
spi.xfer([0x1B, 0xC7])
spi.xfer([0x18, 0xE8])

try:
    for i in range(1):
        val = spi.xfer([0x86, 0x00])
        print(val[1])
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

print(type(val[1]))