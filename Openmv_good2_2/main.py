#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
import sensor, image, time, math, struct,utime
import json
from pyb import LED,Timer,Pin,ExtInt
from struct import pack, unpack
import Message,LineFollowing,DotFollowing
#初始化镜头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置相机模块的像素模式
sensor.set_framesize(sensor.QQVGA)#设置相机分辨率160*120
sensor.skip_frames(time=3000)#时钟
sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡
clock = time.clock()#初始化时钟
#配置引脚，初始化为高电平（此时蜂鸣器不响）。
p_out = Pin('P7', Pin.OUT_PP)
p_out.low()#设置p_out引脚为高

wait_state = 1



class Cnt(object):
    cnt_1 = [0]

#中断函数。
def callback_1():
    #print(1)
    if(Cnt.cnt_1[0] == 0):
        Cnt.cnt_1[0] = 1
    elif(Cnt.cnt_1[0] == 1):
        Cnt.cnt_1[0] = 0

callback_2 = lambda e: callback_1()
#主循环

#给灯起个名字。
class Led(object):
    red_led   = LED(1)

    green_led = LED(2)

    blue_led  = LED(3)

    ir_led    = LED(4)



#中断引脚设置
ext_1 = ExtInt(Pin('P0'), ExtInt.IRQ_FALLING, Pin.PULL_NONE,callback_2)
#开启中断
ext_1.enable()
p_in = Pin('P0', Pin.IN, Pin.PULL_UP)#设置p_in为输入引脚，并开启上拉电阻


takeoff_switch = 1
while(True):
    clock.tick()#时钟初始化

    DotFollowing.Isblob() #检测是否有色块

      #检测任务模式，闪灯。
    if(Cnt.cnt_1[0] == 0):
        Led.red_led.off()
        Led.blue_led.off()
        #无任务，闪绿灯。
        Led.green_led.on()
        takeoff_switch = 1
        Message.Nothing()#传数据，告诉飞机什么都不做。

    elif(Cnt.cnt_1[0] == 1):
        Led.blue_led.off()
        Led.green_led.off()

        #任务一，闪红灯
        Led.red_led.on()#一键起飞，开始任务。
        if takeoff_switch :
            Message.takeoff()#是0x43
            print('take off')


    if (Cnt.cnt_1[0] == 1) :#点检测
        #DotFollowing.DotCheck()
        print('任务一，闪红灯',utime.localtime())
    elif (Cnt.cnt_1[0] == 0):
        print('无任务，闪绿灯。',utime.localtime())

    if (DotFollowing.Dot.blob_state and (Cnt.cnt_1[0] == 1)):
        p_out.high()#开启蜂鸣器
        print('good')
        takeoff_switch = 0
        # if wait_state:
        Message.Waiting()
        sensor.snapshot().save("example_1.jpg") # or "example.bmp" (or others)
        sensor.snapshot().save("example_2.jpg")
        sensor.snapshot().save("example_3.jpg")
            # print('wait')
            # wait_state = 0
    elif(DotFollowing.Dot.blob_state != 1) :
        p_out.low()#关闭蜂鸣器
        print('bad')

    #用户数据发送
    #Message.UartSendData(Message.UserDataPack(127,127,32767,32767,65536,65536,65536,65536,65536,65536))
    #计算程序运行频率
    # if Message.Ctr.IsDebug == 1:
        # fps=int(clock.fps())
        # Message.Ctr.T_ms = (int)(1000/fps)
        # print('fps',fps,'T_ms',Message.Ctr.T_ms)

#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
