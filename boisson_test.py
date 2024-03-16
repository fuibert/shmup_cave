from gpiozero import LED, Button
import time

relay = LED(17)
led = LED(22)
receiver = Button(27)

try:
    from gpiozero import LED, Button
    while True:
        led.on()
        time.sleep(0.1)
        if receiver.is_pressed :
            print("glouglou")
            relay.on()
        else:
            print("pas glouglou")
            relay.off()
      #  relay.on()
        
except KeyboardInterrupt:
    pass
relay.off()
led.off()