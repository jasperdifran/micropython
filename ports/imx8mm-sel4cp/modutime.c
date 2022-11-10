/**
 * @file modutime.c
 * @author Jasper Di Francesco (jasper.difrancesco@gmail.com)
 * @brief MicroPython time module for imx8mm board
 * @version 0.1
 * @date 2022-10-20
 *
 * @copyright Copyright (c) 2022
 *
 */

#include <stdio.h>
#include "py/builtin.h"
#include "py/runtime.h"
#include <unistd.h>
#include <time.h>

STATIC mp_obj_t py_utime_ticks_ms(void)
{
    return mp_obj_new_int(time(NULL));
}

STATIC MP_DEFINE_CONST_FUN_OBJ_0(utime_ticks_ms_obj, py_utime_ticks_ms);

STATIC const mp_rom_map_elem_t mp_module_utime_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_utime)},
    {MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&utime_ticks_ms_obj)},
};

STATIC MP_DEFINE_CONST_DICT(mp_module_utime_globals, mp_module_utime_globals_table);

const mp_obj_module_t mp_module_utime = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mp_module_utime_globals,
};

MP_REGISTER_MODULE(MP_QSTR_utime, mp_module_utime);