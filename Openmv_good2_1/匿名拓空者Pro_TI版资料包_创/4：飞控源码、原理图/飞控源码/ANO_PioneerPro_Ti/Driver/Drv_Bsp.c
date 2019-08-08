#include "Drv_Bsp.h"
#include "pwm.h"
#include "Drv_RcIn.h"
#include "Drv_Spi.h"
#include "Drv_Led.h"
#include "Drv_Paramter.h"
#include "Drv_icm20602.h"
#include "drv_ak8975.h"
#include "drv_spl06.h"
#include "Drv_PwmOut.h"
#include "Drv_Adc.h"
#include "Drv_Uart.h"
#include "Ano_FcData.h"
#include "Ano_Sensor_Basic.h"
#include "Ano_RC.h"
#include "Ano_FlightCtrl.h"
#include "Drv_gps.h"
#include "ano_usb.h"
#include "Drv_UP_Flow.h"
#include "Drv_laser.h"

static uint64_t SysRunTimeMs = 0;

void SysTick_Init(void )
{
	ROM_SysTickPeriodSet(ROM_SysCtlClockGet()/1000);
	ROM_SysTickIntEnable();
	ROM_SysTickEnable();
}
void SysTick_Handler(void)
{
	SysRunTimeMs++;
}
uint32_t GetSysRunTimeMs(void)
{
	return SysRunTimeMs;
}
uint32_t GetSysRunTimeUs(void)
{
	return SysRunTimeMs*1000 + (SysTick->LOAD - SysTick->VAL) * 1000 / SysTick->LOAD;
}

void MyDelayMs(u32 time)
{
	ROM_SysCtlDelay(80000 * time /3);
}

void Drv_SenserCsPinInit(void)
{
	Drv_Icm20602CSPinInit();
	Drv_AK8975CSPinInit();
	Drv_SPL06CSPinInit();
	
	ROM_SysCtlPeripheralEnable(FLASH_CSPIN_SYSCTL);
	ROM_GPIOPinTypeGPIOOutput(FLASH_CS_PORT,FLASH_CS_PIN);
	ROM_GPIOPinWrite(FLASH_CS_PORT, FLASH_CS_PIN,FLASH_CS_PIN);
}

u8 of_init_type;
void Drv_BspInit(void)
{
	/*����ϵͳ��ƵΪ80M*/
	ROM_SysCtlClockSet(SYSCTL_SYSDIV_2_5 | SYSCTL_USE_PLL | SYSCTL_XTAL_16MHZ |SYSCTL_OSC_MAIN);
	/*�ж����ȼ��������*/
	NVIC_SetPriorityGrouping(0x03);
	/*�����������㵥Ԫ*/	
	ROM_FPULazyStackingEnable();
	ROM_FPUEnable();
	
	//����USB���⴮�ڳ�ʼ��
	AnoUsbCdcInit();	
	//�ȳ�ʼ���������ڣ��Ա�ͨ��
	Drv_Uart2Init(500000);	//������
	//���ݳ�ʼ��
	Dvr_ParamterInit();
	//��ȡ��ʼ����
	Para_Data_Init();
	//�ƹ��ʼ��
	Dvr_LedInit();
	
	//ң�ؽ���ģʽ��ʼ��
	Remote_Control_Init();

	//spiͨ�ų�ʼ��
	Drv_Spi0Init();
	Drv_SenserCsPinInit();
	//��ʼ��ICM
	sens_hd_check.acc_ok = sens_hd_check.gyro_ok =
	Drv_Icm20602Init();
	//��ʼ����ѹ��
	sens_hd_check.baro_ok = Drv_Spl0601Init();
	//�������OK���������̲�������㣨ע���˴�û���������Ƿ������ļ�����
	sens_hd_check.mag_ok = 1;       //	
	
	//��������ʼ��
	Drv_PwmOutInit();
	//ADC��ʼ��
	Drv_AdcInit();
	//�δ�ʱ�ӳ�ʼ��
	SysTick_Init();	
	//���ڳ�ʼ��
	//
	Drv_Uart3Init(500000);  //��OPMV
	Drv_GpsPin_Init();//
	//	
	Drv_Uart4Init(19200);	//���������
	Drv_Uart5Init(115200);//�Ӵ��ʼ���	
//	MyDelayMs(200);	
	//���������ʼ��
	of_init_type = (Drv_OFInit()==0)?0:2;
	if(of_init_type==2)//���������ʼ���ɹ�
	{
		//���ʼ����ʼ��
		Drv_Laser_Init();	
	}
	else if(of_init_type==0)//���������ʼ��ʧ��
	{
		Drv_Uart4Init(500000);	//����������
	}
	//====fc
	//�ɿش����������ʼ��
	Sensor_Basic_Init();	
	//�ɿ�PID��ʼ��
	All_PID_Init();
}




