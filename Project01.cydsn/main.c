/* ========================================
 *
 * Alfonso Massimo, Canavate Chloé, Franke Patrick
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include "project.h"
#include <stdio.h>

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    /* Place your initialization/startup code here (e.g. MyInst_Start()) */
    UART_BT_Start();        // UART for bluetooth communication    
    UART_Debug_Start();     // UART for debugging purposes
    
    
    // Bluetooth Communication Check
    UART_BT_PutString("UART BT: Communication started.\r\n");
    uint8_t count = 0;
    char buffer[50];

    for(;;)
    {
        /* Place your application code here. */
        
        // Bluetooth Output to CoolTerm
        sprintf(buffer, "Count = %d\r\n", count);
        UART_BT_PutString(buffer);
        count++;
        CyDelay(1000);
    }
}

/* [] END OF FILE */
