from gpiozero import LED, Button
import time
from  io_cave import *


def old() :
    relay = LED(17)#26 
    led = LED(22)
    receiver = Button(27)

    try:
        while True:
            led.on()
            time.sleep(0.1)
            if receiver.is_pressed :
                print("glouglou")
                relay.on()
            else:
                print("pas glouglou zzzzzzzzzzzzzz")
                relay.off()
            
            
    except KeyboardInterrupt:
        pass
    relay.off()
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