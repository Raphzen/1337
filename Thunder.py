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
#from Blynk import *
#import BlynkLib
#import main
from threading import Thread
import threading

# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

global strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, strip_type=ws.WS2811_STRIP_GRB)
strip.begin()


from flask import Flask
from flask_restful import Api, Resource , reqparse

# API FLASK
app = Flask(__name__)
api = Api(app)




#Test von Return value im multithreading
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return

    

# class controller(Resource):
#     def get(self,status):
#         if (status == "On" ):
#             On(strip)
#             return "superOn" ,200
#         if (status == "Off" ):
#             Off(strip)
#             return "superOff" ,200
#         return "scheisseOff" , 404


# # api.add_resource(controller, "/TurnOn/<string:status>")



Actual_Mode="Initialize"

def rotate(array, n):
    array = (array[len(array) - n:len(array)]  
            + array[0:len(array) - n]) 

def weather():
    weather_com_result=pywapi.get_weather_from_weather_com('SNXX0006')
    #temperature=int(weather_com_result['current_conditions']['temperature'])
    #temp_f=temperature * 9 / 5 + 32
    #humidity=int(weather_com_result['current_conditions']['humidity'])
    #wind_speed=int(weather_com_result['current_conditions']['wind'])
    Current_Conditions=weather_com_result['current_conditions']['text']
    return Current_Conditions

weather_thread=threading.Thread(target=weather) 



##HIER WEITERMACHEN:
def Static(strip):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,0, 0, 0)
    strip.show()
    

#
#Color_Array = []
#for i in range(0, LED_COUNT-1):
#    Color_Array.append(i)


def Off(strip):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,Color(0,0,0))
    strip.show()

def On(strip):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,Color(255,255,255))
    strip.show()


def Reset(strip):
    Color_Array = []
    run_once=0
    if run_once==0:
        for i in range(0, strip.numPixels()):
            Color_Array.append(i)
            Color_Array[i]=Color(0,0,0)
            strip.setPixelColor(i, Color_Array[i])
        run_once=1

def Rain(strip):
    Color_Array = []
    for i in range(0, strip.numPixels()):
            Color_Array.append(i)
    while True:
        Rain_x=randint(40,50)
        for l in range(0, Rain_x):
            for m in range(0, strip.numPixels()):
                strip.setPixelColor(m, Color_Array[m])
            strip.show()
            Color_Array = (Color_Array[len(Color_Array) - 1:len(Color_Array)]  #weiterschieben
                    + Color_Array[0:len(Color_Array) - 1]) 
            time.sleep(25/1000.0)
            Color_Array[0]=Color(13,80,250)


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
    while State(value=="Thunder"):    
        wait_ms=randint(2, 10)
        time.sleep(wait_ms)
        ######old code below#######
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
    def SetSky(strip):
        for i in range(0, strip.numPixels()):
            Color_Array.append(i)
            Color_Array[i]=Color(13,80,250)
            strip.setPixelColor(i, Color_Array[i])
    SetSky(strip)
    while True:
        Cloud=randint(15,30)
        Sky=randint(10,20)
        for j in range(0, Cloud):
            Color_Array[1]=Color(120,120,120)
            for k in range(0, strip.numPixels()):
                strip.setPixelColor(k, Color_Array[k])
            strip.show()
            
            Color_Array = (Color_Array[len(Color_Array) - 1:len(Color_Array)]  
                    + Color_Array[0:len(Color_Array) - 1]) 
            time.sleep(100/1000.0)
        for l in range(0, Sky):
            Color_Array[1]=Color(13,80,250)
            for m in range(0, strip.numPixels()):
                strip.setPixelColor(m, Color_Array[m])
            strip.show()
            Color_Array = (Color_Array[len(Color_Array) - 1:len(Color_Array)]  
                    + Color_Array[0:len(Color_Array) - 1]) 
            time.sleep(100/1000.0)
           
def Partly_Cloudy(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i+q, (255,255,255))
    strip.show()
    

@app.route('/State/<string:value>')
def State(value):
    global strip
    if (value=="Off"):
        Off(strip)
        return "LED OFF", 200
    if (value=="On"):
        On(strip)
        return "LED ON", 200
    while (value=="Thunder"):
        Reset(strip)
        thunder(strip)
        return "Thunder", 200
    if (value=="Mostly_Cloudy"):
        Reset(strip)
        Mostly_Cloudy(strip)
        return "Mostly Cloudy", 200
    if (value=="Rain"):
        Reset(strip)
        Rain(strip)
        return "Rain", 200
    
    return "", 404

#@app.route('/RGB/<string:Color>')
#def RGB(rgb)
    #string "255,100,199" komma trennen und jeden wert zu r g und b zuweisen
    

app.run(debug=True)



# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()



    # Create NeoPixel object with appropriate configuration.
    #strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, strip_type=ws.WS2811_STRIP_GRB)
    # Intialize the library (must be called once before other functions).
    #strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        #Start Threads
        weather_thread.start()


        start_time=0
        while True:
            Current_Conditions=weather_thread.join()
            #print(Current_Conditions)
            '''
            current_time=time.time()
            if (current_time-start_time)>300:
                ###Durch weather() ersetzen 

                start_time=time.time()
                weather_com_result=pywapi.get_weather_from_weather_com('SNXX0006')
                temperature=int(weather_com_result['current_conditions']['temperature'])
                temp_f=temperature * 9 / 5 + 32
                humidity=int(weather_com_result['current_conditions']['humidity'])
                Current_Conditions=weather_com_result['current_conditions']['text']
                #beaufort = int(weather_com_result['wind']['speed'])
                print("Aktuelles Wetter: " + Current_Conditions)
                #print("Windgeschwindigkeit: " + beaufort)
            '''

            #Current_Conditions="Rain"
            ### Aktuellen Wetter Modus speichern: wenn der Modus==den Current Conditions:
                ### kein erneuter Funktionsaufruf wegen Zuruecksetzen der LEDs
            if Actual_Mode!="T-Storm":    
                if Current_Conditions=="T-Storm":
                    Actual_Mode="T-Storm"
                    wait_ms=randint(2, 10)
                    print(wait_ms)
                    time.sleep(wait_ms)
                    print( "Thunder animations!")
                    thunder(strip)
                    if randint(0,10) >8:
                        thunder(strip)
                    if randint(0,10) >8:
                        thunder(strip)

            if Current_Conditions=="Rain":
                Reset(strip)
                Rain(strip)


            if Current_Conditions=="Heavy T-Storm":
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
            if Actual_Mode!="Mostly Cloudy":  ### schriebt einmal den Funktionsaufruf. Im aufruf keine schleife.
                                                ### schleife wieder einfuehren und bei neuem Actual Mode einen Break des Loops       
                if Current_Conditions=="Mostly Cloudy":
                    Actual_Mode="Mostly Cloudy"
                    Mostly_Cloudy(strip)
                    
            if Current_Conditions=="Partly Cloudy":
                Partly_Cloudy(strip)
                
            current_time=time.time()


    except KeyboardInterrupt:
        if args.clear:
            for i in range(0, strip.numPixels()):
                strip.setPixelColor(i, Color(0,0,0))
            strip.show()
