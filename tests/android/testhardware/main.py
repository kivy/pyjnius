from time import sleep
from jnius import autoclass

print('-- test hardware start!')

Hardware = autoclass('org.renpy.android.Hardware')
print('DPI is', Hardware.getDPI())

Hardware.accelerometerEnable(True)
for x in range(20):
    print(Hardware.accelerometerReading())
    sleep(.1)

print('-- test hardware done!')
