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
import LED_Modes
import API



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