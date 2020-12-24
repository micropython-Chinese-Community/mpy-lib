'''
    mpy drive for NTC thermistor Sensor

    Author: shaoziyang
    Date:   2020.12

    http://www.micropython.org.cn

'''
import math

def NTC(adc, B=3780, bits=12):
    t1 = math.log(adc/((1<<bits)-adc))/B + 1/298.15
    return 1/t1 - 273.15