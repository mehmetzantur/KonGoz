#!/usr/bin/python
from subprocess import Popen
import sys
 
filename = '/home/pi/Desktop/github/KonGoz/Kongoz_Engine.py'
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()
