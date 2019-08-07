#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
from pyb import LED,Timer
import sensor, image, time, math, struct
import Message
Red_threshold =(59, 76, 40, 75, 0, 87)#  寻色块用 红色
Blue_threshold =(0, 48, -20, 59, -66, -28)#  寻色块用 蓝色
Green_threshold =(30, 100, -64, -8, -32, 32)#  寻色块用 蓝色

#Yelow_threshold = (59, 76, 40, 75, 0, 87)#  寻色块用 

class Dot(object):
    flag = 0
    color = 0
    x = 0
    y = 0
    
    blob_state = 0
    
    
Dot=Dot()

def Isblob():
    img = sensor.snapshot(line_filter = LineFilter)#拍一张图像
    red_blobs = img.find_blobs([Red_threshold], pixels_threshold=3, area_threshold=3, merge=True, margin=5)#识别红色物体
    if red_blobs:
        Dot.blob_state = 1
    else:
        Dot.blob_state = 0

#色块识别函数
#定义函数：找到画面中最大的指定色块
def FindMax(blobs):
    max_size=1
    if blobs:
        max_blob = 0
        for blob in blobs:
            blob_size = blob.w()*blob.h()
            if ( (blob_size > max_size) & (blob_size > 100)   ) :#& (blob.density()<1.2*math.pi/4) & (blob.density()>0.8*math.pi/4)
                if ( math.fabs( blob.w() / blob.h() - 1 ) < 2.0 ) :
                    max_blob=blob
                    max_size = blob.w()*blob.h()
        return max_blob

def LineFilter(src, dst):
  for i in range(0, len(dst), 1):
      dst[i] = src[i<<1]

#点检测
def DotCheck():
    img = sensor.snapshot(line_filter = LineFilter)#拍一张图像
    red_blobs = img.find_blobs([Red_threshold], pixels_threshold=3, area_threshold=3, merge=True, margin=5)#识别红色物体
    max_blob=FindMax(red_blobs)#找到最大的那个
    if max_blob:
        img.draw_cross(max_blob.cx(), max_blob.cy())#物体中心画十字
        img.draw_rectangle(max_blob.rect())#画圈
        #获取坐标并转换为+-200
        Dot.x = max_blob.cx()-80
        Dot.y = max_blob.cy()-60
        Dot.flag = 1
        #LED灯闪烁
        LED(3).toggle()
        #LED灯闪烁
        LED(2).toggle()
    else:
        Dot.flag = 0
        LED(2).off()
        LED(3).off()
    Message.UartSendData(Message.DotDataPack(Dot.color,Dot.flag,Dot.x,Dot.y,Message.Ctr.T_ms))
    return Dot.flag
    #串口发送数据给飞控



#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
