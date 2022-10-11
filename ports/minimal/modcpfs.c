/**
 * @file modcpfs.c
 * @author Jasper Di Francesco
 * @brief Simple file system which piggybacks off memzip for the core platform
 * @version 0.1
 * @date 2022-10-06
 * 
 * @copyright Copyright (c) 2022
 * 
 */

// #ifdef MICROPY_CPFS

#include "py/builtin.h"
#include "py/runtime.h"
#include <unistd.h>

#include <shared/memzip/memzip.h>

STATIC mp_obj_t py_cpfs_info(void) {
    return mp_obj_new_str("Core Platform File System", 24);
}

MP_DEFINE_CONST_FUN_OBJ_0(cpfs_info_obj, py_cpfs_info);

STATIC mp_obj_t py_cpfs_readfile(mp_obj_t filename_in) {
    const char *filename = mp_obj_str_get_str(filename_in);
    void *data = NULL;
    size_t len = 0;

    memzip_locate(filename, &data, &len);

    return mp_obj_new_bytearray_by_ref(len, data);
}

MP_DEFINE_CONST_FUN_OBJ_1(cpfs_readfile_obj, py_cpfs_readfile);

STATIC mp_obj_t py_cpfs_stat(mp_obj_t filename_in) {
    const char *filename = mp_obj_str_get_str(filename_in);

    MEMZIP_FILE_INFO res;

    if (memzip_stat(filename, &res) == MZ_NO_FILE) {
        return MP_OBJ_NEW_SMALL_INT(1);
    }

    return mp_obj_new_tuple(4, (mp_obj_t[]) {
        mp_obj_new_int(res.file_size),
        mp_obj_new_int(res.last_mod_date),
        mp_obj_new_int(res.last_mod_time),
        mp_obj_new_int(res.is_dir)
    });
}

MP_DEFINE_CONST_FUN_OBJ_1(cpfs_stat_obj, py_cpfs_stat);

STATIC const mp_rom_map_elem_t mp_module_cpfs_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_cpfs) },
    { MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&cpfs_info_obj) },
    { MP_ROM_QSTR(MP_QSTR_readfile), MP_ROM_PTR(&cpfs_readfile_obj) },
    { MP_ROM_QSTR(MP_QSTR_stat), MP_ROM_PTR(&cpfs_stat_obj) },
};

STATIC MP_DEFINE_CONST_DICT(mp_module_cpfs_globals, mp_module_cpfs_globals_table);

const mp_obj_module_t mp_module_cpfs = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mp_module_cpfs_globals,
};

MP_REGISTER_MODULE(MP_QSTR_cpfs, mp_module_cpfs);

// #endif