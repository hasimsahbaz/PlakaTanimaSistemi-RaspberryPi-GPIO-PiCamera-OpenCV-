import os
import cv2
import kamera
from time import sleep
#from picamera import PiCamera
import imutils
import pytesseract
import numpy as np
#import RPi.GPIO as GPIO

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(11, GPIO.OUT)
    a=0
    while True:
        i=GPIO.input(7)

        if i==1:
            print("Gelen VAR"), i
            GPIO.output(11, 1)
            kamera.goruntu()
            sleep(1)
        elif i==0:
             print("Gelen Giden YOK"),i
             GPIO.output(11,0)
             sleep(1)
if __name__=='__main__':
    main()