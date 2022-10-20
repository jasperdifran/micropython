#include <unistd.h>

void run_webserver(char *rx_buf, char *tx_buf, unsigned int *len);

void imx_putc(uint8_t ch);

void init_websrv();