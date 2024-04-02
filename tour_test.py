from gpiozero import LED, Button, OutputDevice
import time
from  io_cave import *


def old() :
    led = LED(16)
    led = LED(23)
    led = LED(24)

    try:
        while True:
            print("led")
            led.on()
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        pass
    led.off()

def new() :
    if not IO_Controller.verre():
        print("en attente d'un verre")
    else:
        print("letzgo")

mode = "old"
if mode == "new" :
    IO_Controller = IO_Controller()
    try:
        while True :
            new()        
    except KeyboardInterrupt:
        pass
else :
    old()