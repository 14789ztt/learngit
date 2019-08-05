#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
import sensor, image, time, math, struct,utime,mjpeg
import json
from pyb import LED,Timer,ExtInt,Pin
from struct import pack, unpack
import Message,LineFollowing,DotFollowing
#初始化镜头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置相机模块的像素模式
sensor.set_framesize(sensor.QQVGA)#设置相机分辨率160*120
sensor.skip_frames(time=3000)#时钟
sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡
clock = time.clock()#初始化时钟



class Cnt(object):
    cnt_1 = [0]


m = mjpeg.Mjpeg("zhang.mjpeg")

video_sta = 1 #video 开启标志位
def video():

    for i in range(10):
        clock.tick()
        m.add_frame(sensor.snapshot())




#中断函数。
def callback_1():
    #print(1)
    if(Cnt.cnt_1[0] == 0):
        Cnt.cnt_1[0] = 1
    elif(Cnt.cnt_1[0] == 1):
        Cnt.cnt_1[0] = 2
    elif(Cnt.cnt_1[0] == 2):
        Cnt.cnt_1[0] = 0

callback_2 = lambda e: callback_1()


#给灯起个名字。
class Led(object):
    red_led   = LED(1)

    green_led = LED(2)

    blue_led  = LED(3)

    ir_led    = LED(4)



#p_in = Pin('P7', Pin.IN, Pin.PULL_UP)#设置p_in为输入引脚，并开启上拉电阻

#中断引脚设置
ext_1 = ExtInt(Pin('P0'), ExtInt.IRQ_FALLING, Pin.PULL_NONE,callback_2)
#开启中断
ext_1.enable()
p_in = Pin('P0', Pin.IN, Pin.PULL_UP)#设置p_in为输入引脚，并开启上拉电阻


#主循环
while(True):



    #检测任务模式，闪灯。
    if(Cnt.cnt_1[0] == 1):
        Led.blue_led.off()
        Led.green_led.off()

        #任务一，闪红灯
        Led.red_led.on()#录制开始


        video_sta = 1 #video 开启标志位
        Message.takeoff()
        video()



    elif(Cnt.cnt_1[0] ==2):
        Led.red_led.off()
        Led.green_led.off()
        #任务二，闪蓝灯
        Led.blue_led.on()

        if (video_sta):
            m.close(clock.fps())
            video_sta = 0#关闭标志位

        # LineFollowing.LineCheck()


    elif(Cnt.cnt_1[0] == 0):
        Led.red_led.off()
        Led.blue_led.off()
        #无任务，闪绿灯。
        Led.green_led.on()

        video_sta = 1 #video 开启标志位



    #time.sleep(2000)
    #Cnt.cnt[0] = 1
    #接收串口数据

    if (Cnt.cnt_1[0] == 1) :#点检测
        #DotFollowing.DotCheck()
        print('任务一，闪红灯',utime.localtime())
    elif (Cnt.cnt_1[0] == 2):#线检测
        #LineFollowing.LineCheck()
        print('任务二，闪蓝灯',utime.localtime())
    elif (Cnt.cnt_1[0] == 0):
        print('无任务，闪绿灯。',utime.localtime())

    #用户数据发送
    #Message.UartSendData(Message.UserDataPack(127,127,32767,32767,65536,65536,65536,65536,65536,65536))
    #计算程序运行频率
    # if Message.Ctr.IsDebug == 1:
        # fps=int(clock.fps())
        # Message.Ctr.T_ms = (int)(1000/fps)
        # print('fps',fps,'T_ms',Message.Ctr.T_ms)

#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
