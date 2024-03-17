from gpiozero import LED, Button
import time
from const import RELAY_PIN, CAPTOR_LED_PIN, RECEIVER_PIN, FAKE_RELAY_PIN, IO_MODE, DUREE_REMPLISSAGE

class IO_Controller():
    def __init__(self):
        if IO_MODE == "RELAY":
            self.output = LED(RELAY_PIN)
        else:
            self.output = LED(FAKE_RELAY_PIN)
            print("FAKE RELAY")
        self.led = LED(CAPTOR_LED_PIN)
        self.receiver = Button(RECEIVER_PIN)
        self.led.on()

    def remplissage(self):
        start_time = time.time()
        try:
            while self.verre() and time.time() < start_time + DUREE_REMPLISSAGE:
                time.sleep(0.1)
                if self.verre():
                    #print("glouglou")
                    self.output.on()
                else:
                    #print("pas glouglou")
                    self.output.off()
                self.output.on()

        except KeyboardInterrupt:
            pass
        self.output.off()
        
    def verre(self):
        return self.receiver.is_pressed

    def reward(self, score):
        print("YOOOOOOOOOOOOLO")
        print("score : ", score)
        self.remplissage()
