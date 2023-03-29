#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <websrvint.h>

#include "py/builtin.h"
#include "py/compile.h"
#include "py/runtime.h"
#include "py/repl.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "shared/runtime/pyexec.h"

void init_websrv()
{
}

#if MICROPY_ENABLE_COMPILER
void do_str(const char *src, mp_parse_input_kind_t input_kind)
{
    nlr_buf_t nlr;
    if (nlr_push(&nlr) == 0)
    {
        mp_lexer_t *lex = mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, src, strlen(src), 0);
        qstr source_name = lex->source_name;
        mp_parse_tree_t parse_tree = mp_parse(lex, input_kind);
        mp_obj_t module_fun = mp_compile(&parse_tree, source_name, true);
        mp_call_function_0(module_fun);
        nlr_pop();
    }
    else
    {
        // uncaught exception
        mp_obj_print_exception(&mp_plat_print, (mp_obj_t)nlr.ret_val);
    }
}
#endif

static char *stack_top;
#if MICROPY_ENABLE_GC
static char heap[2048 * 128] = {0};
#endif

/* Buffer for us to read from and write to */
char *rx_buffer;
char *tx_buffer;
unsigned int *tx_length;

void run_webserver(char *rx_buf, char *tx_buf, unsigned int *len)
{
    int stack_dummy;
    stack_top = (char *)&stack_dummy;
    rx_buffer = rx_buf;
    tx_buffer = tx_buf;
    tx_length = len;

    gc_init(heap, heap + sizeof(heap));
    mp_init();

    int status = pyexec_file_if_exists("websrv.py");
    if (status != 0) {
        printf("Exited!\n");
    }

    mp_deinit();
    return;
}

#if MICROPY_ENABLE_GC
void gc_collect(void)
{
    // WARNING: This gc_collect implementation doesn't try to get root
    // pointers from CPU registers, and thus may function incorrectly.
    void *dummy;
    gc_collect_start();
    gc_collect_root(&dummy, ((mp_uint_t)stack_top - (mp_uint_t)&dummy) / sizeof(mp_uint_t));
    gc_collect_end();
    gc_dump_info();
}
#endif

// mp_lexer_t *mp_lexer_new_from_file(const char *filename) {
//     mp_raise_OSError(MP_ENOENT);
// }

// mp_import_stat_t mp_import_stat(const char *path) {
//     return MP_IMPORT_STAT_NO_EXIST;
// }

void nlr_jump_fail(void *val)
{
    while (1)
    {
        ;
    }
}

void NORETURN __fatal_error(const char *msg)
{
    while (1)
    {
        ;
    }
}

#ifndef NDEBUG
void MP_WEAK __assert_func(const char *file, int line, const char *func, const char *expr)
{
    printf("Assertion '%s' failed, at file %s:%d\n", expr, file, line);
    __fatal_error("Assertion failed");
}
#endif
