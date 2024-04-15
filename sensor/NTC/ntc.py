'''
    mpy drive for NTC thermistor Sensor

    Author: shaoziyang
    Date:   2024.4

    http://www.micropython.org.cn

'''
import math

def NTC_GND(adc, max, B=3780):
    t1 = math.log(adc/(max-adc))/B + 1/298.15
    return 1/t1 - 273.15

def NTC_VCC(adc, max, B=3780):
    t1 = math.log((max-adc)/adc)/B + 1/298.15
    return 1/t1 - 273.15
