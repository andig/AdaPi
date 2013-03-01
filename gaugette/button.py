import wiringpi
import time

class Button:
    
    # button states
    OFF     = 0     # button inactive (not pressed)
    PRESS   = 1     # button pressed and quickly released
    LONG    = 2     # button pressed and still held
    ACTIVE  = 3     # button pressed but not yet released (internal state)
    
    def __init__(self, pin, longpress=0.3):
        self.pin = pin
        self.longpress = longpress
        self.state = Button.OFF
        self.io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
        self.io.pinMode(self.pin, self.io.INPUT)
        self.io.pullUpDnControl(self.pin, self.io.PUD_UP)

    def get_state(self):
        state = self.io.digitalRead(self.pin) ^ 1       # low-active
        
        # button state model
        if self.state == Button.PRESS: self.state = Button.OFF
        
        if self.state == Button.OFF and state:
            self.state = Button.ACTIVE
            self.pressed = time.time()
        elif self.state == Button.ACTIVE: 
            if state:
                if time.time()-self.pressed >= self.longpress: self.state = Button.LONG
            else:
                self.state = Button.PRESS
        elif self.state == Button.LONG and not state:
            self.state = Button.OFF

        #if self.state not in [Button.OFF, Button.ACTIVE]: print("Button: %s" % ["OFF","PRESS","LONG","ACTIVE"][self.state])
        return self.state
