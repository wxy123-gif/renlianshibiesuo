#ifndef __USART3_H
#define __USART3_H

#include "sys.h"

#define FACE_UART_MAX_RECV_LEN     64
#define AS608_UART_MAX_RECV_LEN   128
#define AS608_BAUD_RATE          57600

extern u8 FaceUart_RxPacket[FACE_UART_MAX_RECV_LEN];
extern vu16 FaceUart_RxSta;

extern u8 USART3_RX_BUF[AS608_UART_MAX_RECV_LEN];
extern vu16 USART3_RX_STA;

void FaceUart_Init(u32 bound);
void FaceUart_SendByte(u8 Byte);
u8 FaceUart_TakeUnlockRequest(void);

void AS608_Uart_Init(u32 bound);
void AS608_Uart_SendByte(u8 Byte);
void AS608_Uart_ClearRx(void);

#endif
