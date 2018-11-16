#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.


import time
from neopixel import *
import argparse
from random import *
import pywapi
import string
import numpy
import array


# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

Current_Conditions=""


def weather():
    weather_com_result=pywapi.get_weather_from_weather_com('SNXX0006')
    temperature=int(weather_com_result['current_conditions']['temperature'])
    temp_f=temperature * 9 / 5 + 32
    humidity=int(weather_com_result['current_conditions']['humidity'])
    Current_Conditions=weather_com_result['current_conditions']['text']


def flash(strip, wait_ms=50):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,Color(125,125,125))
    strip.show()
    time.sleep(wait_ms/100)
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,0)
    strip.show()
    time.sleep(wait_ms/500)
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,Color(255,255,255))
    strip.show()
    time.sleep(wait_ms/1000)
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,0)
    strip.show()   
        
def thunder(strip, wait_ms=numpy.random.uniform(0.01,0.1)):
    random_Position=randint(0, strip.numPixels())
    for Length in range(randint(10, 40)):
        strip.setPixelColor(random_Position+Length, Color(255,255,255))
        strip.show()
        time.sleep(wait_ms/10000)
        #strip.setPixelColor(random_Position+Length, 0)
        #strip.show()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()        
    if randint(0,100)>10:
        flash(strip)
           
def Mostly_Cloudy(strip):
    
    Color_Array = []
    run_once=0
    #erst CLoud dann Sky dann Cloud dann Sky
    strip.setPixelColor(1, Color(255,255,255))
    if run_once==0:
        for i in range(0, strip.numPixels()):
            Color_Array.append(i)
            Color_Array[i]=Color(0,0,255)
            strip.setPixelColor(i, Color_Array[i])
        run_once=1
    while 1:
        Cloud=randint(30,40)
        Sky=randint(2,10)
        for j in range(0, Cloud):
            Color_Array[1]=Color(255,255,255)
            for k in range(0, strip.numPixels()):
                strip.setPixelColor(k, Color_Array[k])
            strip.show()
            
            Color_Array = (Color_Array[len(Color_Array) - 1:len(Color_Array)]  
                    + Color_Array[0:len(Color_Array) - 1]) 
            time.sleep(100/1000.0)
        for l in range(0, Sky):
            Color_Array[1]=Color(0,0,255)
            for m in range(0, strip.numPixels()):
                strip.setPixelColor(m, Color_Array[m])
            strip.show()
            Color_Array = (Color_Array[len(Color_Array) - 1:len(Color_Array)]  
                    + Color_Array[0:len(Color_Array) - 1]) 
            time.sleep(100/1000.0)

        

    
    
    #for i in range(-Cloud, strip.numPixels()):
     #   for x in range(randint(2,10)):
      #      for q in range(Cloud):
       #         strip.setPixelColor(i+q, Color(255,255,255))
        #    strip.show()
         #   time.sleep(100/1000.0)
          #  for i in range(-Cloud, strip.numPixels()):
           #     strip.setPixelColor(i+q, Color(120,50,255))
                    
def Partly_Cloudy(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i+q, (255,255,255))
    strip.show()
    
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

    try:
        start_time=0
        while True:
            current_time=time.time()
            if (current_time-start_time)>3:
                start_time=time.time()
                weather_com_result=pywapi.get_weather_from_weather_com('SNXX0006')
                temperature=int(weather_com_result['current_conditions']['temperature'])
                temp_f=temperature * 9 / 5 + 32
                humidity=int(weather_com_result['current_conditions']['humidity'])
                Current_Conditions=weather_com_result['current_conditions']['text']
                print("Aktuelles Wetter: " + Current_Conditions)

            Current_Conditions="Mostly Cloudy"

            if Current_Conditions=="T-Storm":
                wait_ms=randint(2, 10)
                print(wait_ms)
                time.sleep(wait_ms)
                print( "Thunder animations!")
                thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                    

            if Current_Conditions=="Heavy T-Storm / Windy":
                wait_ms=randint(2, 10)
                print(wait_ms)
                time.sleep(wait_ms)
                print( "Thunder animations!")
                thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)


            if Current_Conditions=="Scattered Thunderstorms":
                wait_ms=randint(2, 10)
                print(wait_ms)
                time.sleep(wait_ms)
                print( "Thunder animations!")
                thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                    
            if Current_Conditions=="Light Rain with Thunder":
                wait_ms=randint(2, 10)
                print(wait_ms)
                time.sleep(wait_ms)
                print( "Thunder animations!")
                thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)       
                    
            if Current_Conditions=="Thunder":
                wait_ms=randint(2, 10)
                print(wait_ms)
                time.sleep(wait_ms)
                print( "Thunder animations!")
                thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)    
            
            if Current_Conditions=="Thunder in the Vicinity":
                wait_ms=randint(2, 10)
                print(wait_ms)
                time.sleep(wait_ms)
                print( "Thunder animations!")
                thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                if randint(0,10) >8:
                    thunder(strip)
                    
            if Current_Conditions=="Mostly Cloudy":
                Mostly_Cloudy(strip)
                    
            if Current_Conditions=="Partly Cloudy":
                Partly_Cloudy(strip)
                
            current_time=time.time()
            #print ('Color wipe animations.')
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print ('Rainbow animations.')
            #rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0))
