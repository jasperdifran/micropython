#include <unistd.h>
#include <websrvint.h>
#include "py/mpconfig.h"

/*
 * Core UART functions to implement for a port
 */

// https://github.com/torvalds/linux/blob/master/drivers/tty/serial/fsl_lpuart.c




#define UARTSTAT 0x98
#define RECEIVE 0x0
#define TRANSMIT 0x40
#define STAT_TDRE (1 << 14)
#define STAT_RDRF  (1 << 0)

extern uint64_t uart_base;
#define UART_REG(x) ((volatile uint32_t *)(uart_base + (x)))

int imx_getc(void)
{
    /* Wait until received. */
    while (!(*UART_REG(UARTSTAT) & STAT_RDRF)) { }
    int val = *UART_REG(RECEIVE);
    // imx_putc((uint8_t)val);
    return val;
}

void imx_putc(uint8_t ch)
{
    while (!(*UART_REG(UARTSTAT) & STAT_TDRE)) { }
    *UART_REG(TRANSMIT) = ch;
}

// Send string of given length
void mp_hal_stdout_tx_strn(const char *str, mp_uint_t len) {
    while (len--) {
        imx_putc(*str++);
    }
}


// Receive single character
int mp_hal_stdin_rx_chr(void) {
    int val = imx_getc();
    imx_putc((uint8_t)val);
    imx_putc('C');
    return val;
}