#include <unistd.h>
#include <websrvint.h>
#include "py/mpconfig.h"

/*
 * Core UART functions to implement for a port
 */

extern uint64_t uart_base;
#define UART_REG(x) ((volatile uint32_t *)(uart_base + (x)))

// Receive single character
int mp_hal_stdin_rx_chr(void) {
    unsigned char c = 0;
    return c;
}

#define STAT 0x98
#define TRANSMIT 0x40
#define STAT_TDRE (1 << 14)

void
imx_putc(uint8_t ch)
{
    while (!(*UART_REG(STAT) & STAT_TDRE)) { }
    *UART_REG(TRANSMIT) = ch;
}

// Send string of given length
void mp_hal_stdout_tx_strn(const char *str, mp_uint_t len) {
    while (len--) {
        imx_putc(*str++);
    }
}
