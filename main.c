#include "stm32f10x.h"                  // Device header
#include "Delay.h"
#include "OLED.h"
#include "Serial.h"
#include"LED.h"

uint8_t RxData;

int main(void)
{
	OLED_Init();
	OLED_ShowString(1, 1, "RxData:");
	LED_Init();
	Serial_Init();
	
	while (1)
	{
		if (Serial_GetRxFlag() == 1)
		{   
			RxData=Serial_GetRxData();
			if(RxData==0x30){
				LED_OFF(GPIOA,GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_6);
			}else if(RxData==0x31){
				LED_ON(GPIOA,GPIO_Pin_1);
				LED_OFF(GPIOA,GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_6);
			}else if(RxData==0x32){
				LED_ON(GPIOA,GPIO_Pin_1 | GPIO_Pin_2);
				LED_OFF(GPIOA,GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_6);
			}else if(RxData==0x33){
				LED_ON(GPIOA,GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3);
				LED_OFF(GPIOA,GPIO_Pin_4 | GPIO_Pin_6);
			}else if(RxData==0x34){
				LED_ON(GPIOA,GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4);
			    LED_OFF(GPIOA,GPIO_Pin_6);
			}else if(RxData==0x35){
				LED_ON(GPIOA,GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_6);
			}else if(RxData==0x36){
				GPIO_Write(GPIOA, ~0x0001);	
				Delay_ms(100);
				GPIO_Write(GPIOA, ~0x0002);	
				Delay_ms(100);
				GPIO_Write(GPIOA, ~0x0004);	
				Delay_ms(100);
				GPIO_Write(GPIOA, ~0x0008);	
				Delay_ms(100);
				GPIO_Write(GPIOA, ~0x0010);
				Delay_ms(100);
				GPIO_Write(GPIOA, ~0x0040);
				Delay_ms(100);
				LED_OFF(GPIOA,GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_6);
			}
			Serial_SendByte(RxData);
			OLED_ShowHexNum(2,1,RxData,2);
//			RxData = Serial_GetRxData();
//			Serial_SendByte(RxData);
//			OLED_ShowHexNum(2, 1, RxData, 2);
//			if(RxData==0x32){
//				OLED_ShowString(3,1,"true");
//			}
		}
	}
}
