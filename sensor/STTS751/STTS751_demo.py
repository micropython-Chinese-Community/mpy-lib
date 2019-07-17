from machine import I2C
import STTS751

i2c = I2C(1)
stt = STTS751.STTS751(i2c)
stt.temperature()
