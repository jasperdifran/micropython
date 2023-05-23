#include <unistd.h>
#include <websrvint.h>
#include "py/mpconfig.h"
#include <stdio.h>

/*
 * Core UART functions to implement for a port
 */

// Send string of given length
void mp_hal_stdout_tx_strn(const char *str, mp_uint_t len)
{
    write(STDOUT_FILENO, str, len);
}

// Receive single character
int mp_hal_stdin_rx_chr(void)
{
    // int val = imx_getc();
    // imx_putc((uint8_t)val);
    // imx_putc('C');
    return 'A'; // Yet to be implemented
}