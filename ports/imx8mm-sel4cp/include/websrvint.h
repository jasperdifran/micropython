#include <unistd.h>

// We are given a 2k buffer to store any data we might need, this is private_data only looked
// at by the webserver (micropython). Each var below len is a pointer to somewhere in the buffer,
// String is null terminated
// int continuation_id; // The id of the continuation
typedef struct
{
    int page_req;
    int addBreadcrumbs;
    int start_time;
    int file_size;
    char *headers;
    char *method;
    char *pagePath;
    char *filePath;
} private_data_t;

typedef struct
{
    void *base;          // Base address of the buffer
    int continuation_id; // The id of the continuation
    unsigned int len;    // The length of the data in the buffer
    char *status;
    char *content_type;
    char *body;
} stat_res_t;

int run_webserver(char *req_buf, void *private_data, char *tx_buf, unsigned int *tx_len);
int run_cont(char *py_file_to_run, int status, void *data, int data_len, void *private_data, char *tx_buf, unsigned int *tx_len);
void imx_putc(uint8_t ch);

// These should be asking for private data, nfs data, a place to write response to and a pointer to a length variable for the response
// From run_webserver and run_cont we return 0 if we are done with the request, 1 if we are waiting on a continuation

void init_websrv();