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
from LED_Modes import *

from flask import Flask #REST API Modul
from flask_restful import Api, Resource , reqparse

# API FLASK
app = Flask(__name__)
api = Api(app)


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