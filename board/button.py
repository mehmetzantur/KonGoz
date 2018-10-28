import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##GPIO.setup(15, GPIO.OUT)
##GPIO.setup(11, GPIO.OUT)

GPIO.setup(7, GPIO.OUT)


while True:
    input_state = GPIO.input(31)
    if input_state == False:
        GPIO.output(7,GPIO.HIGH)
        time.sleep(3)
        GPIO.output(7,GPIO.LOW)
        print('Button Pressed 31')
        time.sleep(0.2)
        
    input_state2 = GPIO.input(33)
    if input_state2 == False:
        print('Button Pressed 33')
        time.sleep(0.2)
    
    
    input_state3 = GPIO.input(35)
    if input_state3 == False:
        print('Button Pressed 35')
        time.sleep(0.2)
        
    input_state4 = GPIO.input(37)
    if input_state4 == False:
        print('Button Pressed 37')
        time.sleep(0.2)