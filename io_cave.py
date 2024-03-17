from gpiozero import LED, Button
import time
from const import RELAY_PIN, CAPTOR_LED_PIN, RECEIVER_PIN, FAKE_RELAY_PIN, IO_MODE

class IO_Controller():
    def __init__(self):
        if IO_MODE == "RELAY":
            self.output = LED(RELAY_PIN)
        else:
            self.output = LED(FAKE_RELAY_PIN)
        self.led = LED(CAPTOR_LED_PIN)
        self.receiver = Button(RECEIVER_PIN)

    def remplissage(self):
        try:
            from gpiozero import LED, Button
            while True:
                self.led.on()
                time.sleep(0.1)
                if self.verre():
                    print("glouglou")
                    self.output.on()
                else:
                    print("pas glouglou")
                    self.output.off()
                self.relay.on()


        except KeyboardInterrupt:
            pass
        self.output.off()
        self.led.off()

    def verre(self):
        return self.receiver.is_pressed

    def reward(score):
        print("YOOOOOOOOOOOOLO")
        print("score : ", score)
