import time
from pyb import Pin



p_out = Pin('P7', Pin.OUT_PP)#设置p_out为输出引脚


p_out.low()#设置p_out引脚为低

time.sleep(1000)

p_out.high()#设置p_out引脚为高
time.sleep(1000)

p_out.low()#设置p_out引脚为低

time.sleep(1000)

p_out.high()#设置p_out引脚为高


# p_in = Pin('P7', Pin.IN, Pin.PULL_UP)#设置p_in为输入引脚，并开启上拉电阻

# value = p_in.value() # get value, 0 or 1#读入p_in引脚的值