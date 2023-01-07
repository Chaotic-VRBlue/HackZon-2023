import time
import os
import spidev
import serial
import RPi.GPIO as GPIO
import numpy

HR_SENSOR = 12
tempFlag = 0
bpFlag = 0
hrFlag = 0

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=5000

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

def ConvertTemp(data,places):
  temp = ((data * 330)/float(1023))#-50 40
  temp = round(temp,places)
  return temp

light_channel = 0
temp_channel  = 0
delay = 1

def readChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def readTempSensor():
    temp = readChannel(0)
    return temp

def SENSOR_READ():
    temp_level = ReadChannel(0)
    temp_volts = ConvertVolts(temp_level,2)
    temp       = ConvertTemp(temp_level,2)
    temp = temp+10;

    ECG_level = ReadChannel(1)
    ECG_volts = ConvertVolts(ECG_level,2)

    print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
    print("ECG: {}".format(ECG_level))
    
    if(temp>35):
      print('More Temperature')
      
    if(ECG_level>500):
      print('ecg Reported')
    time.sleep(delay)   
    
while True:

    SENSOR_READ()
