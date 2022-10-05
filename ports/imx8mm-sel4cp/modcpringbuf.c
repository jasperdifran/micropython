#include "py/builtin.h"
#include "py/runtime.h"
#include <unistd.h>

/**
 * @brief Module to manage passing strings between C and Python
 * 
 */


#if MICROPY_PY_CPRINGBUF

extern char *data_buf;

STATIC mp_obj_t py_cpringbuf_info(void) {
    return mp_obj_new_str("cpringbuf", 9);
}
MP_DEFINE_CONST_FUN_OBJ_0(cpringbuf_info_obj, py_cpringbuf_info);

STATIC mp_obj_t py_cpringbuf_rx(void) {
    for (int i = 0;;i++) {
        if (data_buf[i] == '\0') {
            return mp_obj_new_str(data_buf, i);
        }
    }
}
MP_DEFINE_CONST_FUN_OBJ_0(cpringbuf_rx_obj, py_cpringbuf_rx);

STATIC mp_obj_t py_cpringbuf_tx(mp_obj_t buf_in) {
    // Copy from str to data_buf
    const char *str = mp_obj_str_get_str(buf_in);
    int i = 0;
    while (str[i] != '\0') {
        data_buf[i] = str[i];
        i++;
    }
    data_buf[i] = '\0';

    return MP_OBJ_NEW_SMALL_INT(0);
}
MP_DEFINE_CONST_FUN_OBJ_1(cpringbuf_tx_obj, py_cpringbuf_tx);



STATIC const mp_rom_map_elem_t mp_module_cpringbuf_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_cpringbuf) },
    { MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&cpringbuf_info_obj) },
    { MP_ROM_QSTR(MP_QSTR_rx), MP_ROM_PTR(&cpringbuf_rx_obj) },
    { MP_ROM_QSTR(MP_QSTR_tx), MP_ROM_PTR(&cpringbuf_tx_obj) },

};

STATIC MP_DEFINE_CONST_DICT(mp_module_cpringbuf_globals, mp_module_cpringbuf_globals_table);

const mp_obj_module_t mp_module_cpringbuf = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mp_module_cpringbuf_globals,
};

MP_REGISTER_MODULE(MP_QSTR_cpringbuf, mp_module_cpringbuf);

#endif