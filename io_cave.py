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

    def remplissage(self, score):
        start_time = time.time()
        score_modifier = self.calculate_score_modifier(score)
        try:
            while self.verre() and time.time() < start_time + DUREE_REMPLISSAGE:
                time.sleep(0.1)
                if self.verre():
                    self.output.on()
                else:
                    self.output.off()
                self.output.on()

        except KeyboardInterrupt:
            pass
        self.output.off()
    def calculate_score_modifier(self, score):
        if score > 50 :
            return 0
        return 2 - (score/25)
    def verre(self):
        return self.receiver.is_pressed

    def reward(self, score):
        self.remplissage(score)
