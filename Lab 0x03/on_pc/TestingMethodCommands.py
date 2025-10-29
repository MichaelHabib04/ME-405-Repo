#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 13:41:10 2025

@author: katherinemeezan
"""

from serial import Serial
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib import pyplot
import csv

times = []
data = []

# ComPort = "/dev/tty.usbmodem2058397458562"   # For MacOS, will need to change if board is reflashed
ComPort = "/dev/tty.usbmodem1103"
# ComPort = "COM13"

"""!
Methods to run data collection
!"""

def read_data(ser):
    data = []
    while True:
        line = ser.readline().decode(errors="replace").strip()
        if "MOTOR:" in line or "Number of data points:" in line or not line:  # or "MICROSEC" in line:
            return data, line
        data.append(line)



def save_csv(filename, data_lines):
    if not data_lines:
        print(f"No data for {filename}")
        return
    header = data_lines[0].split(",")
    rows = [line.split(",") for line in data_lines[1:] if "," in line]
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([h.strip() for h in header])
        for row in rows:
            writer.writerow([x.strip() for x in row])
    print(f"Saved {len(rows)} rows to {filename}")


"""!
Below are methods to write commands to run things from the UI Task

UI Task guide:
    r = increase right motor effort by 10
    e = decrease right motor effort by 10
    l = increase left motor effort by 10
    k = decrease left motor effort by 10
    c = enable/disable right motor
    n = enable/disable left motor
    p = print current motor efforts
    s = run step response test
    b = print current task state (for debugging, can remove)
    z = print output of test data
   
    v = reset right and left motor efforts to 0
    d = zero right motor effort
    h = zero left motor effort
    q = inc right motor effort by 1
    w = inc left motor effort by 1
    t = dec right motor effort by 1
    x = dec left motor effort by 1
    
    u = multiply current right motor effort by 10
    m = multiply current left motor effort by 10

Motor step response test:
    Turns both motors off
    Sets both motor efforts to what the right motor effort currently is
    Runs for ~2.5 to 3 seconds
    Turns both motors off (effort does not reset)
    Sets run share to start/stop data collection (data collection is not working)
!"""

def incReff10():
    ser.write(b"r\r\n")

def decReff10():
    ser.write(b"e\r\n")
    
def incLeff10():
    ser.write(b"l\r\n")
    
def decLeff10():
    ser.write(b"k\r\n")
    
def enableRmot():
    ser.write(b"c\r\n")
    
def enableLmot():
    ser.write(b"n\r\n")
    
def enableMots():
    enableRmot()
    enableLmot()
    

def writeS():
    ser.write(b"s\r\n")

def getTestResults():
    ser.write(b"\z\r\n")

def zeroMotEfforts():
    ser.write(b"\v\r\n")
    
def zeroRmot():
    ser.write(b"d\r\n")
def zeroLmot():
    ser.write(b"h\r\n")

def incReff():
    ser.write(b"q\r\n")
def decReff():
    ser.write(b"t\r\n")
def incLeff():
    ser.write(b"w\r\n")
def decLeff():
    ser.write(b"x\r\n")
    
def rEffx10():
    ser.write(b"u\r\n")
def lEffx10():
    ser.write(b"\m\r\n")

"""!
Below are methods to have Romi move in certain ways, or to run specific tests
!"""
def setRMotEff(eff):
    zeroRmot()
    ones = eff%10
    tens = eff//10
    if eff>0:
        for i in range(tens):
            incReff10()
        for i in range(ones):
            incReff()
    if eff<0:
        for i in range(tens):
            decReff10()
        for i in range(ones):
            decReff()

def setLMotEff(eff):
    zeroLmot()
    ones = eff%10
    tens = eff//10
    if eff>0:
        for i in range(tens):
            incLeff10()
        for i in range(ones):
            incLeff()
    if eff<0:
        for i in range(tens):
            decLeff10()
        for i in range(ones):
            decLeff()
            

def straightLineTest10(eff):  # For an effort that is a multiple of 10
    zeroMotEfforts()
    numR = eff // 10
    #ser.write(b"c\r\n")
    for i in range(numR):
        incReff10()
    writeS()

def pivotInPlaceClockwise(eff):   # For an effort that is a multiple of 10
    zeroMotEfforts()
    numR = eff // 10
    for i in range(numR):
        decReff10()
        incLeff10()

def pivotInPlaceCCwise(eff):   # For an effort that is a multiple of 10
    numR = eff // 10
    for i in range(numR):
        incReff10()
        decLeff10()
        


"""!
Below is code to run Romi from a com port
!"""



with Serial(ComPort, baudrate=115_200, timeout=1) as ser:
    print("Opening serial port")
    sleep(0.5)

    print("Sending Ctrl-C to break into REPL...")
    ser.write(b"\x03")  # Ctrl-C
    sleep(0.5)

    print("Sending Ctrl-D to soft reboot and run main.py...")
    ser.write(b"\x04")  # Ctrl-D
    sleep(1)

    print("Flushing serial port")
    while ser.in_waiting:
        ser.read()
        
    
    
    # print("Sending command to start data collection")
    setRMotEff(13)
    setLMotEff(25)