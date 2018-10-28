import RPi.GPIO as GPIO
import time


def blink1(pin):
    
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.1)
        
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.1)
        
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.1)
        
        return
    
def blink2(pin):
            
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.1)
        
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.1)
        
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.1)
        
        return
    
    
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

for i in range(0,50):
        blink1(11)
        blink2(15)
GPIO.cleanup()