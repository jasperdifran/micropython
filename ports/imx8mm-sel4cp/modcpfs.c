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
#include <stdio.h>
#include <unistd.h>

#include <shared/memzip/memzip.h>

typedef unsigned int sel4cp_channel;

void req_file(const char *filename, int len_to_read);
void stat_file(const char *filename);

STATIC mp_obj_t py_cpfs_info(void)
{
    return mp_obj_new_str("Core Platform File System", 24);
}

MP_DEFINE_CONST_FUN_OBJ_0(cpfs_info_obj, py_cpfs_info);

STATIC mp_obj_t py_cpfs_readfile(mp_obj_t filename_in)
{
    const char *filename = mp_obj_str_get_str(filename_in);
    void *data = NULL;
    size_t len = 0;

    // stat_file("otherfile");

    // printf("Reading a file, about to notify\n");
    // req_file("somfile");
    // printf("Notified\n");

    MEMZIP_RESULT err = memzip_locate(filename, &data, &len);
    if (err != MZ_OK)
    {
        return MP_OBJ_NEW_SMALL_INT(1);
    }

    return mp_obj_new_bytearray_by_ref(len, data);
}

MP_DEFINE_CONST_FUN_OBJ_1(cpfs_readfile_obj, py_cpfs_readfile);

STATIC mp_obj_t py_cpfs_readfileasync(mp_obj_t filename_in, mp_obj_t len_to_read)
{
    (void)filename_in;
    // const char *filename = mp_obj_str_get_str(filename_in);
    // void *data = NULL;
    // size_t len = 0;

    // stat_file("otherfile");

    const char *filename = mp_obj_str_get_str(filename_in);
    req_file(filename, mp_obj_get_int(len_to_read));

    // MEMZIP_RESULT err = memzip_locate(filename, &data, &len);
    // if (err != MZ_OK)
    // {
    //     return MP_OBJ_NEW_SMALL_INT(1);
    // }

    return MP_OBJ_NEW_SMALL_INT(0);
}

MP_DEFINE_CONST_FUN_OBJ_2(cpfs_readfileasync_obj, py_cpfs_readfileasync);

STATIC mp_obj_t py_cpfs_stat(mp_obj_t filename_in)
{
    const char *filename = mp_obj_str_get_str(filename_in);

    MEMZIP_FILE_INFO res;

    if (memzip_stat(filename, &res) == MZ_NO_FILE)
    {
        // mp_obj_print_exception(&mp_plat_print, mp_obj_new_str("File not found", 14));
        return MP_OBJ_NEW_SMALL_INT(1);
    }

    return mp_obj_new_tuple(4, (mp_obj_t[]){
                                   mp_obj_new_int(res.file_size),
                                   mp_obj_new_int(res.last_mod_date),
                                   mp_obj_new_int(res.last_mod_time),
                                   mp_obj_new_int(res.is_dir)});
}

MP_DEFINE_CONST_FUN_OBJ_1(cpfs_stat_obj, py_cpfs_stat);

STATIC mp_obj_t py_cpfs_statasync(mp_obj_t filename_in)
{
    const char *filename = mp_obj_str_get_str(filename_in);

    stat_file(filename);
    return MP_OBJ_NEW_SMALL_INT(0);
}

MP_DEFINE_CONST_FUN_OBJ_1(cpfs_statasync_obj, py_cpfs_statasync);

STATIC mp_obj_t py_cpfs_exists(mp_obj_t filename_in)
{
    const char *filename = mp_obj_str_get_str(filename_in);

    MEMZIP_FILE_INFO res;

    if (memzip_stat(filename, &res) == MZ_NO_FILE)
    {
        return mp_const_false;
    }

    return mp_const_true;
}

MP_DEFINE_CONST_FUN_OBJ_1(cpfs_exists_obj, py_cpfs_exists);

STATIC const mp_rom_map_elem_t mp_module_cpfs_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_cpfs)},
    {MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&cpfs_info_obj)},
    {MP_ROM_QSTR(MP_QSTR_readfile), MP_ROM_PTR(&cpfs_readfile_obj)},
    {MP_ROM_QSTR(MP_QSTR_readfileasync), MP_ROM_PTR(&cpfs_readfileasync_obj)},
    {MP_ROM_QSTR(MP_QSTR_stat), MP_ROM_PTR(&cpfs_stat_obj)},
    {MP_ROM_QSTR(MP_QSTR_statasync), MP_ROM_PTR(&cpfs_statasync_obj)},
    {MP_ROM_QSTR(MP_QSTR_exists), MP_ROM_PTR(&cpfs_exists_obj)},
};

STATIC MP_DEFINE_CONST_DICT(mp_module_cpfs_globals, mp_module_cpfs_globals_table);

const mp_obj_module_t mp_module_cpfs = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mp_module_cpfs_globals,
};

MP_REGISTER_MODULE(MP_QSTR_cpfs, mp_module_cpfs);

// #endif