#ifndef __ANO_LED_H
#define __ANO_LED_H

//==����
#include "sysconfig.h"


//==����
enum  //led���
{
	X_led = 0,
	B_led,
	R_led,
	G_led,
	LED_NUM,
};

#define BIT_NULLLED 0x00		
#define BIT_XLED 0x01		//�ɿ�LED
#define BIT_BLED 0x02		//��ɫ
#define BIT_RLED 0x04		//��ɫ
#define BIT_GLED 0x08		//��ɫ
#define BIT_WLED 0x0e		//��ɫ
#define BIT_PLED 0x06		//��ɫ
#define BIT_YLED 0x0c		//��ɫ

typedef struct 
{
	u8 allOk;
	u8 lowVt;//�͵�ѹ
	u8 rst_imu;
	u8 calGyr;
	u8 calAcc;
	u8 calMag;
	u8 calHz;	//У׼ˮƽ��
	u8 errMpu;
	u8 errMag;
	u8 errBaro;
	u8 errOneTime;	//������ʾ
	u8 noRc;	//ʧ��
	u8 staOf;	//����״̬
	u8 staGps;	//GPS״̬
	u8 saving;	//����������
}_led_sta;




//==��������
extern _led_sta LED_STA;

//==��������

//static


//public
void Drv_LED_Init(void);
void LED_1ms_DRV(void );
void LED_Task(u8);
void LED_Task(u8 dT_ms);
void LED_Task2(u8 dT_ms);







#endif
