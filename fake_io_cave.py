import time
from const import RELAY_PIN, CAPTOR_LED_PIN, RECEIVER_PIN, FAKE_RELAY_PIN, IO_MODE, DUREE_REMPLISSAGE, FAKE_GODET_IS_LA
from tkinter import *

class Fake_output():
    def __init__(self, mytype):
        self.mytype = mytype
        self.is_pressed = FAKE_GODET_IS_LA
    def on(self):
        print("ALLUMAGE DE ", self.mytype)
    def off(self):
        print("EXTINCTION DE ", self.mytype)
class Fake_IO_Controller():
    def __init__(self):
        if IO_MODE == "RELAY":
            self.output = Fake_output("RELAY")
        else:
            self.output = Fake_output("RELAY")
            print("FAKE RELAY")
        self.led = Fake_output("LED")
        self.receiver = Fake_output("BUTTON")
        self.led.on()

    def remplissage(self, score):
        start_time = time.time()
        score_modifier = self.calculate_score_modifier(score)
        try:
            while self.verre() and time.time() < start_time + DUREE_REMPLISSAGE - score_modifier:
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
