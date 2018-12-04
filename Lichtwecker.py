#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.


import datetime
import time
from neopixel import *
import argparse
from random import *
import pywapi
import string
import numpy
import gTTS
import wave 
import StringIO 
from picotts import PicoTTS


# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
Wake_Up   = "04:50:00"
TTS_Time = "05:05:00"


           
def Lichtwecker(strip):
    x=0
    for start_time in range(0, 255):
        #print(start_time)
        #print(time.strftime("%X"))
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i, Color(255,209,163))
            strip.setBrightness(x)
        x=x+1
        strip.show()
        time.sleep(2.35)      
        
def weather():
    weather_com_result=pywapi.get_weather_from_weather_com('SNXX0006')
    temperature=int(weather_com_result['current_conditions']['temperature'])
    temp_f=temperature * 9 / 5 + 32
    humidity=int(weather_com_result['current_conditions']['humidity'])
    Current_Conditions=weather_com_result['current_conditions']['text']
    
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')


    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()


    try:
        while True:
            current_day=datetime.datetime.today().weekday()
            current_time=str(time.strftime("%X"))
            if current_time == Wake_Up and current_day in (0,1,2,3,4):
                Lichtwecker(strip)
            if current_time == TTS_Time:
                picotts = PicoTTS() 
                wavs = picotts.synth_wav(‘Guten Morgen Rafael!’) 
                wav = wave.open(StringIO.StringIO(wavs)) 
                print wav.getnchannels(), wav.getframerate(), wav.getnframes()
            if current_time == "05:30:00":
                for i in range(0, strip.numPixels()):
                    strip.setPixelColor(i, Color(0,0,0))
                strip.show()

    except KeyboardInterrupt:
        if args.clear:
            for i in range(0, strip.numPixels()):
                strip.setPixelColor(i, Color(0,0,0))
            strip.show()