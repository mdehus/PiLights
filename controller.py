import RPi.GPIO as GPIO
import random
import time
import math

GPIO.setmode(GPIO.BOARD)

class LED(object):
    def __init__(self, pin, on=GPIO.HIGH, off=GPIO.LOW):
        self.pin = pin
        self.on = on
        self.off = off
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 120)
        self.max_brightness = 100
        self.turn_off()

    def turn_on(self, brightness=100):
        if brightness == self.max_brightness:
            GPIO.output(self.pin, self.on) 
        else:  
            self.pwm.start(brightness)

    def turn_off(self):
        self.pwm.stop()
        GPIO.output(self.pin, self.off)

    def fade_on(self, brightness=0, speed=.0005):
        self.pwm.start(brightness)
        while brightness < 100:
            brightness += 1
            new_duty = 1 / (1 + math.exp(-((brightness / 16) - 6))) * 100
            #print brightness, new_duty
            self.pwm.ChangeDutyCycle(brightness)
            time.sleep(speed)

    def fade_off(self, brightness=100, speed=.0005):
        while brightness > 0:
            brightness -= 1
            self.pwm.ChangeDutyCycle(brightness)
            time.sleep(speed)
            

class RGB_LED(object):
    def __init__(self, red_led, green_led, blue_led):
        self.red_led = red_led
        self.blue_led = blue_led
        self.green_led = green_led    

    def turn_on(self, red=255, green=255, blue=255):
        if red > 0:
            self.red_led.turn_on()
        
        if green > 0:
            self.green_led.turn_on()

        if blue > 0:
            self.blue_led.turn_on()

class FiveRGBLEDController(object):
    def __init__(self):
        self.blue_leds = [LED(3), LED(13), LED(21), LED(24), LED(16)]
        self.green_leds = [LED(5), LED(15), LED(23), LED(22), LED(10)]
        self.red_leds = [LED(7), LED(19), LED(26), LED(18), LED(8)]
        self.all_leds = self.blue_leds + self.green_leds + self.red_leds
        self.colors = ["red_leds", "green_leds", "blue_leds"]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        GPIO.cleanup()

    def random_sparkle(self, count=100, action="fade", n_leds=5, pause=0.5, fade_speed=.00005):
        if action == "fade":
            kwargs = {"speed":fade_speed}

        for i in range(0, count):
            randset = random.sample(self.all_leds, n_leds)
            [getattr(led, action + "_on")(**kwargs) for led in randset]
            time.sleep(pause)
            [getattr(led, action + "_off")(**kwargs) for led in randset]

    def spectrum_analyzer(self, color, bg=None, count=20, speed=0.0005):
        leds = getattr(self, color)
        if bg is not None:
            bg_leds = getattr(self, bg)
            [led.turn_on() for led in bg_leds]

        for i in range(0, count):
            height = random.randint(0, 5)
            [led.fade_on(speed=speed) for led in leds[:height]]
            [led.fade_off(speed=speed) for led in reversed(leds[:height])]

        if bg is not None:
            self.all_off()
         
    def flash(self, color, count=10, pause=0.05):
        ''' Turn LEDs on, wait a brief pause, then off.
        '''
        leds = getattr(self, color)

        for i in range(0, count):
            [led.turn_on() for led in leds]
            time.sleep(pause)
            [led.turn_off() for led in leds]
            time.sleep(pause)

    def ping_pong(self, color, bg=None, count=1, fade_speed=.00009):
        ''' Fades LEDS from one end back to the other.
        '''
        leds = getattr(self, color)
        
        for i in range(0, count):
            #[led.fade_on(speed=fade_speed) for led in leds]
            #[led.fade_off(speed=fade_speed) for led in leds]
            #[led.fade_on(speed=fade_speed) for led in reversed(leds)]
            #[led.fade_off(speed=fade_speed) for led in reversed(leds)]
            self.walk(color, bg, reverse=False, count=1, fade_speed=fade_speed)
            self.walk(color, bg, reverse=True, count=1, fade_speed=fade_speed)

    def crazy_disco_party(self, count, pause=.03):
        '''  Rapidly flashes random colors n number of times.
        '''
        last_color = None

        for i in range(0, count):
            while True:
                color = random.choice(self.colors)
                if color != last_color:
                    last_color = color
                    break

            self.flash(color, count=3, wait_time=wait_time)

    def walk(self, color, bg=None, reverse=False, count=1, fade_speed=.0005):
        leds = getattr(self, color)
        if bg is not None:
            bg_leds = getattr(self, bg)
            [led.turn_on() for led in bg_leds]
        
        if reversed:
            [led.fade_on(speed=fade_speed) for led in reversed(leds)]
            [led.fade_off(speed=fade_speed) for led in reversed(leds)]
        else:
            [led.fade_on(speed=fade_speed) for led in leds]
            [led.fade_off(speed=fade_speed) for led in leds]

        if bg is not None:
            self.all_off()

    def all_off(self):
        [led.turn_off() for led in self.all_leds]

def main():
    blue_leds = [LED(3), LED(13), LED(21), LED(24), LED(16)]
    green_leds = [LED(5), LED(15), LED(23), LED(22), LED(10)]
    red_leds = [LED(7), LED(19), LED(26), LED(18), LED(8)]
    all_leds = blue_leds + green_leds + red_leds

    [led.turn_on() for led in all_leds]
    raw_input("Press enter to start the show")
    [led.turn_off() for led in all_leds]

    #for i in range(0, 20):
    #    led = random.choice(all_leds)
    #    led.fade_on(speed=.01)
    #    time.sleep(.5)
    #    led.fade_off(speed=.01)
    for i in range(0, 10):
        rand_leds = [random.choice(all_leds) for i in range(5)]
        [led.turn_on() for led in rand_leds]
        time.sleep(.5)
        [led.turn_off() for led in rand_leds]

    [led.turn_on() for led in red_leds]
    for i in range(0, 20):
        height = random.randint(0, 5)
        [led.fade_on() for led in green_leds[:height]]
        [led.fade_off() for led in reversed(green_leds[:height])]
        #red_leds[1].fade_on()
        #red_leds[1].fade_off()

    [led.turn_on() for led in blue_leds]
    for i in range(0, 100):
        led = random.choice(all_leds)
        led.fade_on()
        led.fade_off()

    for i in range(0, 100):
        led = random.choice(all_leds)
        led.turn_on()
        time.sleep(.05)
        led.turn_off()

    for i in range(0, 10):
        [led.turn_on() for led in red_leds]
        time.sleep(.05)
        [led.turn_off() for led in red_leds]
        time.sleep(.05)

    for i in range(0, 10):
        [led.turn_on() for led in green_leds]
        time.sleep(.05)
        [led.turn_off() for led in green_leds]
        time.sleep(.05)

    for i in range(0, 10):
        [led.turn_on() for led in blue_leds]
        time.sleep(.05)
        [led.turn_off() for led in blue_leds]
        time.sleep(.05)

    #rgb_led1 = RGB_LED(red_leds[0], blue_leds[0], green_leds[0])
    #rgb_led1.turn_on(0, 0, 255)

    [led.turn_off() for led in all_leds]

    raw_input("Press enter to continue")
    GPIO.cleanup()

if __name__ == '__main__':
    main()

'''
for r,g,b in zip(RED_LEDS, GREEN_LEDS, BLUE_LEDS):
    print r,g,b
    GPIO.setup(r, GPIO.OUT)
    GPIO.setup(g, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)

for r,g,b in zip(RED_LEDS, GREEN_LEDS, BLUE_LEDS):
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.LOW)

#for r,g,b in zip(RED_LEDS, GREEN_LEDS, BLUE_LEDS):
#GPIO.output(r, GPIO.HIGH)
#GPIO.output(g, GPIO.HIGH)
#GPIO.output(b, GPIO.HIGH)

for i in range(0, 3):
    GPIO.output(random.choice(BLUE_LEDS), GPIO.HIGH)
    GPIO.output(random.choice(RED_LEDS), GPIO.HIGH)
    GPIO.output(random.choice(GREEN_LEDS), GPIO.HIGH)

[GPIO.output(led, GPIO.HIGH) for led in RED_LEDS]
time.sleep(1)

for x in range(0, 4):
    for i, led in enumerate(BLUE_LEDS):
        GPIO.output(BLUE_LEDS[i - 1], GPIO.LOW)
        GPIO.output(RED_LEDS[i], GPIO.LOW)
        GPIO.output(led, GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(RED_LEDS[i], GPIO.HIGH)

'''
