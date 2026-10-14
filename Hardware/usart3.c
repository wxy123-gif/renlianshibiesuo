#include "stm32f10x.h"
#include "usart3.h"
#include "timer.h"
#include <stdio.h>

u8 FaceUart_RxPacket[FACE_UART_MAX_RECV_LEN];
vu16 FaceUart_RxSta = 0;
static volatile u8 FaceUart_UnlockRequest = 0;

u8 USART3_RX_BUF[AS608_UART_MAX_RECV_LEN];
vu16 USART3_RX_STA = 0;

static u8 As608RxState = 0;
static u16 As608RxIndex = 0;
static u16 As608RxTotal = 0;

static void As608RxReset(void)
{
    As608RxState = 0;
    As608RxIndex = 0;
    As608RxTotal = 0;
}

void FaceUart_Init(u32 bound)
{
    GPIO_InitTypeDef GPIO_InitStructure;
    USART_InitTypeDef USART_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_AFIO, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    USART_InitStructure.USART_BaudRate = bound;
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;
    USART_InitStructure.USART_StopBits = USART_StopBits_1;
    USART_InitStructure.USART_Parity = USART_Parity_No;
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;
    USART_Init(USART2, &USART_InitStructure);

    USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);

    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);

    USART_Cmd(USART2, ENABLE);

    FaceUart_RxSta = 0;
    FaceUart_UnlockRequest = 0;

    TIM2_Int_Init(99, 7199);
    TIM_Cmd(TIM2, DISABLE);
}

void FaceUart_SendByte(u8 Byte)
{
    USART_SendData(USART2, Byte);
    while (USART_GetFlagStatus(USART2, USART_FLAG_TXE) == RESET);
}

int fputc(int ch, FILE *f)
{
    (void)f;
    FaceUart_SendByte((u8)ch);
    return ch;
}

u8 FaceUart_TakeUnlockRequest(void)
{
    u8 request = FaceUart_UnlockRequest;
    FaceUart_UnlockRequest = 0;
    return request;
}

void USART2_IRQHandler(void)
{
    u8 data;
    u16 length;

    if (USART_GetITStatus(USART2, USART_IT_RXNE) != RESET)
    {
        data = (u8)USART_ReceiveData(USART2);
        length = FaceUart_RxSta & 0x7FFF;

        if ((FaceUart_RxSta & 0x8000) == 0 && length < FACE_UART_MAX_RECV_LEN)
        {
            if (length == 0)
            {
                TIM_Cmd(TIM2, ENABLE);
            }
            TIM_SetCounter(TIM2, 0);
            FaceUart_RxPacket[FaceUart_RxSta & 0x7FFF] = data;
            FaceUart_RxSta = (FaceUart_RxSta & 0x8000) | ((FaceUart_RxSta & 0x7FFF) + 1);
        }

        length = FaceUart_RxSta & 0x7FFF;
        if (length >= 4 &&
            FaceUart_RxPacket[0] == 0xFF &&
            FaceUart_RxPacket[1] == 0xAB &&
            FaceUart_RxPacket[2] == 0xCD &&
            FaceUart_RxPacket[3] == 0xFE)
        {
            FaceUart_UnlockRequest = 1;
            FaceUart_RxSta = 0;
            TIM_Cmd(TIM2, DISABLE);
        }
        else if ((FaceUart_RxSta & 0x8000) != 0)
        {
            FaceUart_RxSta = 0;
        }

        USART_ClearITPendingBit(USART2, USART_IT_RXNE);
    }
}

void AS608_Uart_Init(u32 bound)
{
    GPIO_InitTypeDef GPIO_InitStructure;
    USART_InitTypeDef USART_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART3, ENABLE);

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_Init(GPIOB, &GPIO_InitStructure);

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_Init(GPIOB, &GPIO_InitStructure);

    USART_InitStructure.USART_BaudRate = bound;
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;
    USART_InitStructure.USART_StopBits = USART_StopBits_1;
    USART_InitStructure.USART_Parity = USART_Parity_No;
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;
    USART_Init(USART3, &USART_InitStructure);

    USART_ITConfig(USART3, USART_IT_RXNE, ENABLE);

    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    NVIC_InitStructure.NVIC_IRQChannel = USART3_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);

    USART_Cmd(USART3, ENABLE);
    AS608_Uart_ClearRx();
}

void AS608_Uart_SendByte(u8 Byte)
{
    USART_SendData(USART3, Byte);
    while (USART_GetFlagStatus(USART3, USART_FLAG_TXE) == RESET);
}

void AS608_Uart_ClearRx(void)
{
    USART3_RX_STA = 0;
    As608RxReset();
}

void USART3_IRQHandler(void)
{
    u8 data;
    u16 packetLength;

    if (USART_GetITStatus(USART3, USART_IT_RXNE) != RESET)
    {
        data = (u8)USART_ReceiveData(USART3);

        if ((USART3_RX_STA & 0x8000) == 0)
        {
            switch (As608RxState)
            {
            case 0:
                if (data == 0xEF)
                {
                    USART3_RX_BUF[0] = data;
                    As608RxIndex = 1;
                    As608RxState = 1;
                }
                break;

            case 1:
                if (data == 0x01)
                {
                    USART3_RX_BUF[1] = data;
                    As608RxIndex = 2;
                    As608RxState = 2;
                }
                else if (data != 0xEF)
                {
                    As608RxReset();
                }
                break;

            case 2:
                if (As608RxIndex < AS608_UART_MAX_RECV_LEN)
                {
                    USART3_RX_BUF[As608RxIndex++] = data;
                }
                else
                {
                    As608RxReset();
                    break;
                }

                if (As608RxIndex >= 9)
                {
                    packetLength = ((u16)USART3_RX_BUF[7] << 8) | USART3_RX_BUF[8];
                    As608RxTotal = 9 + packetLength;
                    if (packetLength < 3 || As608RxTotal > AS608_UART_MAX_RECV_LEN)
                    {
                        As608RxReset();
                    }
                    else
                    {
                        As608RxState = 3;
                        if (As608RxIndex >= As608RxTotal)
                        {
                            USART3_RX_STA = 0x8000 | As608RxTotal;
                            As608RxReset();
                        }
                    }
                }
                break;

            case 3:
                if (As608RxIndex < AS608_UART_MAX_RECV_LEN)
                {
                    USART3_RX_BUF[As608RxIndex++] = data;
                }
                else
                {
                    As608RxReset();
                    break;
                }

                if (As608RxIndex >= As608RxTotal)
                {
                    USART3_RX_STA = 0x8000 | As608RxTotal;
                    As608RxReset();
                }
                break;

            default:
                As608RxReset();
                break;
            }
        }

        USART_ClearITPendingBit(USART3, USART_IT_RXNE);
    }
}
