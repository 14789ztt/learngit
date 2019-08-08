#include "Drv_heating.h"
#include "Drv_PwmOut.h"
//void Drv_HeatingInit(void)
//{

//}

void Drv_HeatingSet(u8 val)
{
	Drv_HeatSet((val*10));
//	if(val > 99)
//		TIM10->CCR1 = 99;
//	else
//		TIM10->CCR1 = val;
}

#include "Ano_DT.h"
#include "Ano_Sensor_Basic.h"
#include "Ano_Parameter.h"
#include "Ano_math.h"

//����λ�����ú��¹��ܿ���  
//#define USE_THERMOSTATIC 
/*
���棺�������Ⱥ��¹���ʱһ������ʹThermostatic_Ctrl_Task����ͣ�����У�
�������κγ����쳣����debug����ʹThermostatic_Ctrl_Taskͣ�����У�
��������ɷɿ�Ӳ���𻵣������ʹ�á�
*/


#define EXP_TEMPERATURE 60
#define TEMPERATURE_KP 2.5f
#define TEMPERATURE_KI 5.0f
#define TEMPERATURE_KD 3.5f

//float test_temperature_ctrl_arg[3] ;
float temperature_fb[3],temperature_err,temperature_err_i,temperature_diff,temperature_ctrl_val;
static u16 temperature_cnt;
static u8 thermostatic_en;
void Thermostatic_Ctrl_Task(u8 dT_ms)
{
	//����ǰ���������
	if(flag.unlock_sta == 0)
	{
		if(Ano_Parame.set.heatSwitch == 1)//�������¹���
		{
			if(thermostatic_en == 0)
			{
				//
				thermostatic_en = 1;
				//��λ��ɱ��
				flag.mems_temperature_ok = 0;
				//
				sensor.acc_z_auto_CALIBRATE = 1; //���¶�׼Z��
				sensor.gyr_CALIBRATE = 2;//����У׼������
				//
				ANO_DT_SendString("Thermostatic ON......");	
			}
		}
		else
		{
			if(thermostatic_en)
			{
				//
				thermostatic_en = 0;
				//
				ANO_DT_SendString("Thermostatic OFF,Please Restart ANO_Pioneer_pro!");	
			}
		}
	}
	
	//
	if(thermostatic_en)
	{
		//�ϴη���
		temperature_fb[1] = temperature_fb[0];
		//���η�����ICM�ڲ��¶ȴ�����
		temperature_fb[0] = sensor.Tempreature_C;
		//΢��
		temperature_diff = (temperature_fb[0] - temperature_fb[1]) *1000/dT_ms;
		//΢�����У���΢��Ԥ�ⷴ����
		temperature_fb[2] = temperature_fb[0] + temperature_diff *TEMPERATURE_KD ;//*test_temperature_ctrl_arg[2];
		//����ƫ��
		temperature_err = EXP_TEMPERATURE - temperature_fb[2];
		//-----
		if(1)//((temperature_ctrl_val)<100)
		{
			//����ƫ���޷�
			temperature_err_i += LIMIT(temperature_err,-10,10) *dT_ms *0.001f;
			//�����޷�
			temperature_err_i = LIMIT(temperature_err_i,-20,20);
		}
		//������������
		temperature_ctrl_val = 
		TEMPERATURE_KP *temperature_err // *test_temperature_ctrl_arg[0]
		+ TEMPERATURE_KI *temperature_err_i;// *test_temperature_ctrl_arg[1];
		//
		temperature_ctrl_val = LIMIT(temperature_ctrl_val ,0,100);
		//���¿��������
		Drv_HeatingSet((u8)temperature_ctrl_val); 
		//�ж��Ƿ���ɺ��µ����¹���
		if(flag.mems_temperature_ok == 0)
		{		
			if(temperature_fb[0] > (EXP_TEMPERATURE-0.2f) && temperature_fb[0] < (EXP_TEMPERATURE+0.2f))
			{
				//ƫ��С��0.2���϶ȣ��ҳ���1500ms���ж��������
				if(temperature_cnt<1500)
				{
					temperature_cnt += dT_ms;
				}
				else
				{

						//
						flag.mems_temperature_ok = 1;
						//
						ANO_DT_SendString("Thermostatic OK!");	
					
				}
			}
			else
			{
				temperature_cnt = 0;
			}
		}
	}
	else //��ʹ�ú��¹���
	{
		flag.mems_temperature_ok = 1;
		Drv_HeatingSet((u8)0); 
	}

}

