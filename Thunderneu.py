import time
from neopixel import *
import argparse
from random import *
import pywapi
import string
import numpy
import array
from multiprocessing import *
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

global weather_thread
global Current_Thread_Mode
global status 

from flask import Flask #REST API Modul
from flask_restful import Api, Resource , reqparse

# API FLASK
app = Flask(__name__)
api = Api(app)

def weather(): #Wetterabruf
    weather_com_result=pywapi.get_weather_from_weather_com('SNXX0006')
    #temperature=int(weather_com_result['current_conditions']['temperature'])
    #temp_f=temperature * 9 / 5 + 32
    #humidity=int(weather_com_result['current_conditions']['humidity'])
    #wind_speed=int(weather_com_result['current_conditions']['wind'])
    Current_Conditions=weather_com_result['current_conditions']['text']
    return Current_Conditions

def Off(strip, value):  #Strip aus
    if value=="Off":
        for i in range(0, strip.numPixels()): #zählt jede LED position durch und setzt den RGB Code auf 0,0,0
            strip.setPixelColor(i,Color(0,0,0))
        strip.show()

def On(strip, value):   #Strip an
    if value=="On":
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i,Color(255,255,255))
        strip.show()

def Reset(strip):   #Reset
    Color_Array = []
    run_once=0
    if run_once==0:
        for i in range(0, strip.numPixels()):
            Color_Array.append(i)
            Color_Array[i]=Color(0,0,0)
            strip.setPixelColor(i, Color_Array[i])
        run_once=1

def flash(strip, wait_ms=50):   #Blitzanimation
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
        
def thunder(strip): #Gewitteranimation
    wait_ms=randint(2, 10)
    time.sleep(wait_ms)
    ######old code below#######
    random_Position=randint(0, strip.numPixels())
    for Length in range(randint(10, 40)):
        strip.setPixelColor(random_Position+Length, Color(255,255,255))
        strip.show()
        time.sleep(wait_ms/10000)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()        
    if randint(0,100)>10:
        flash(strip)
           
def Mostly_Cloudy(strip,value):     #Wolkenmodus
    Color_Array = []        #Farben werden im Color_Array gespeichert
    def SetSky(strip):
        for i in range(0, strip.numPixels()):
            Color_Array.append(i)
            Color_Array[i]=Color(13,80,250)
            strip.setPixelColor(i, Color_Array[i])
    SetSky(strip)
    while value=="Mostly_Cloudy": #Diese Loop sollte unterbrochen werden, sobald ein neuer STeuerbefehl kommt.
        Cloud=randint(15,30) #Variable Wolken Größe
        Sky=randint(10,20)  #Variable Himmel Größe --> Anzahl der LEDs die durchlaufen
        for j in range(0, Cloud):
            Color_Array[1]=Color(120,120,120)
            for k in range(0, strip.numPixels()):
                strip.setPixelColor(k, Color_Array[k])
            strip.show()
            
            Color_Array = (Color_Array[len(Color_Array) - 1:len(Color_Array)]  
                    + Color_Array[0:len(Color_Array) - 1]) #alle Einträge werden eine Position weiter geschoben
            time.sleep(100/1000.0)
        for l in range(0, Sky):
            Color_Array[1]=Color(13,80,250)
            for m in range(0, strip.numPixels()):
                strip.setPixelColor(m, Color_Array[m])
            strip.show()
            Color_Array = (Color_Array[len(Color_Array) - 1:len(Color_Array)]  
                    + Color_Array[0:len(Color_Array) - 1]) 
            time.sleep(100/1000.0)


#REST API
#Hier werden die Values eingegeben, die im Terminal eingegeben werden.
@app.route('/State/<string:value>')
def State(value):
    global strip
    if (value=="Off"):
        Off(strip, value)
        return "LED OFF", 200
    if (value=="On"):
        On(strip, value)
        return "LED ON", 200
    if (value=="Thunder"):
        while (value=="Thunder"):
            Reset(strip)
            thunder(strip)
            return "Thunder", 200
    if (value=="Mostly_Cloudy"):
        Mode=value
        Reset(strip)
        MC=Process(target=Mostly_Cloudy, args=(strip, value,)) #Multiprocess wird gestartet
        MC.daemon=False
        MC.start()
        return "Mostly Cloudy", 200
    if (value!=Mode):
        MC.terminate()
        MC.join
    if (value=="Rain"):
        Reset(strip)
        Rain(strip)
        return "Rain", 200
    
    return "", 404

        
def start_Flask():
    app.run(debug=True)


# Main program logic follows:
if __name__ == '__main__':
    global weather_thread
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    global status
    #status=Value('i',1)
    global weather_thread
    


    #hier sollte der wetter multiprocess gestartet werden.
    #weather_thread=Process(target=update_weather, args=(status,))
    #weather_thread.daemon=False
    #weather_thread.start()
    sF=Process(target=start_Flask)
    sF.daemon=False
    sF.start()

    