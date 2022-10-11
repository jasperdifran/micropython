#include "py/builtin.h"
#include "py/runtime.h"
#include <unistd.h>
#include <stdio.h>

#include <shared/memzip/memzip.h>

/**
 * @brief Module to manage passing strings between C and Python
 * 
 */


// #if MICROPY_PY_cptxrx

extern char rx_datas[];
extern char tx_datas[];
extern unsigned int *tx_length;

STATIC mp_obj_t py_cptxrx_info(void) {
    return mp_obj_new_str("Core Platform TXRX", 19);
}
MP_DEFINE_CONST_FUN_OBJ_0(cptxrx_info_obj, py_cptxrx_info);

STATIC mp_obj_t py_cptxrx_rx(void) {
    for (int i = 0;;i++) {
        if (rx_datas[i] == '\0') {
            return mp_obj_new_bytearray_by_ref(i, rx_datas);
        }
    }
}
MP_DEFINE_CONST_FUN_OBJ_0(cptxrx_rx_obj, py_cptxrx_rx);

STATIC mp_obj_t py_cptxrx_tx(mp_obj_t buf_in) {
    // Copy from str to data_buf
    const char *str = mp_obj_str_get_str(buf_in);
    int bytes_written = 0;
    while (str[bytes_written] != '\0') {
        tx_datas[*tx_length + bytes_written] = str[bytes_written];
        bytes_written++;
    }
    *tx_length += bytes_written;
    tx_datas[*tx_length] = '\0';

    return MP_OBJ_NEW_SMALL_INT(0);
}
MP_DEFINE_CONST_FUN_OBJ_1(cptxrx_tx_obj, py_cptxrx_tx);

STATIC mp_obj_t py_cptxrx_txfile(mp_obj_t filename_in) {
    const char *filename = mp_obj_str_get_str(filename_in);
    void *data = NULL;
    size_t file_len = 0;

    memzip_locate(filename, &data, &file_len);
    char *data_char = (char *)data;
    int bytes_written;
    for (bytes_written = 0; bytes_written < file_len; bytes_written++) {
        tx_datas[bytes_written + *tx_length] = data_char[bytes_written];
    }
    *tx_length += bytes_written;
    tx_datas[*tx_length] = '\0';

    return MP_OBJ_NEW_SMALL_INT(0);
}

MP_DEFINE_CONST_FUN_OBJ_1(cptxrx_txfile_obj, py_cptxrx_txfile);

STATIC const mp_rom_map_elem_t mp_module_cptxrx_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_cptxrx) },
    { MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&cptxrx_info_obj) },
    { MP_ROM_QSTR(MP_QSTR_rx), MP_ROM_PTR(&cptxrx_rx_obj) },
    { MP_ROM_QSTR(MP_QSTR_tx), MP_ROM_PTR(&cptxrx_tx_obj) },
    { MP_ROM_QSTR(MP_QSTR_txfile), MP_ROM_PTR(&cptxrx_txfile_obj) },

};

STATIC MP_DEFINE_CONST_DICT(mp_module_cptxrx_globals, mp_module_cptxrx_globals_table);

const mp_obj_module_t mp_module_cptxrx = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mp_module_cptxrx_globals,
};

MP_REGISTER_MODULE(MP_QSTR_cptxrx, mp_module_cptxrx);

// #endif