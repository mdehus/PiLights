import RPi.GPIO as GPIO
import allleds
import time

def main():
    with allleds.FiveRGBLEDController() as rgbctl:
        rgbctl.random_sparkle(count=5, pause=.05, n_leds=1, fade_speed=.0135)
        #rgbctl.ping_pong("red_leds", count=1, fade_speed=.00005)
        rgbctl.walk("blue_leds", reverse=True, fade_speed=.0003)
        rgbctl.spectrum_analyzer("blue_leds", count=1, speed=.0002)
        rgbctl.spectrum_analyzer("blue_leds", count=8, speed=.001)
        rgbctl.spectrum_analyzer("blue_leds", count=8, speed=.0005)
        rgbctl.ping_pong("red_leds", count=3)
        rgbctl.flash("red_leds")
        rgbctl.flash("green_leds")
        rgbctl.flash("blue_leds")
        rgbctl.flash("red_leds")
        rgbctl.flash("blue_leds")
        rgbctl.flash("green_leds", count=10, pause=.03)
        rgbctl.flash("red_leds", count=10, pause=.03)
        rgbctl.flash("blue_leds", count=10, pause=.03)
        rgbctl.flash("red_leds", count=5, pause=.03)
        rgbctl.flash("green_leds", count=5, pause=.03)
        rgbctl.crazy_disco_shit(9)
        rgbctl.flash("all_leds", count=40, pause=.03)

if __name__ == '__main__':
    main()
