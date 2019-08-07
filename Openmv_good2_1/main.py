#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
import sensor, image, time, math, struct
import json
from pyb import LED,Timer,Pin
from struct import pack, unpack
import Message,LineFollowing,DotFollowing
#初始化镜头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置相机模块的像素模式
sensor.set_framesize(sensor.QQVGA)#设置相机分辨率160*120
sensor.skip_frames(time=3000)#时钟
sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡

#配置引脚，初始化为高电平（此时蜂鸣器不响）。
p_out = Pin('P7', Pin.OUT_PP)
p_out.low()#设置p_out引脚为低

wait_state = 1
clock = time.clock()#初始化时钟

#主循环

while(True):
    clock.tick()#时钟初始化
    
    DotFollowing.Isblob() #检测是否有色块。
    
    #接收串口数据
    # Message.UartReadBuffer()
    if DotFollowing.Dot.blob_state:
        p_out.high()#开启蜂鸣器
        #print('good')
        #if wait_state:
        Message.Waiting()
            
        sensor.snapshot().save("example_1.jpg") # or "example.bmp" (or others)
        sensor.snapshot().save("example_2.jpg")
        sensor.snapshot().save("example_3.jpg")
        print('wait')
            
            #wait_state = 0
           
    else:
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
