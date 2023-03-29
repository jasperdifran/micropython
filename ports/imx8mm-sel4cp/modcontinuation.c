/**
 * @file modcontinuation.c
 * @author Jasper Di Francesco
 * @brief Module for using continuations in micropython. Includes an implementation of pickle, specifically for the request object type.
 * @version 0.1
 * @date 2023-03-29
 *
 * @copyright Copyright (c) 2023
 *
 */

// #ifdef MICROpy_continuation

#include "py/builtin.h"
#include "py/runtime.h"
#include <stdio.h>
#include <unistd.h>

#include <shared/memzip/memzip.h>

typedef unsigned int sel4cp_channel;
extern void *cont_data_store;
extern int cont_done;

STATIC mp_obj_t py_continuation_info(void)
{
    return mp_obj_new_str("Continuation management", 24);
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_info_obj, py_continuation_info);

// STATIC mp_obj_t py_continuation_storereq()
// {
//     void *data = cont_data_store;
// }

STATIC mp_obj_t py_continuation_storereq(mp_obj_t o_in)
{
    printf("Storing request\n");
    const char *method = mp_obj_str_get_str(mp_obj_dict_get(o_in, mp_obj_new_str("method", 6)));
    const char *path = mp_obj_str_get_str(mp_obj_dict_get(o_in, mp_obj_new_str("path", 4)));

    printf("Storing request ");
    printf(method);
    printf(":");
    printf(path);
    printf("\n");
    return MP_OBJ_SMALL_INT_VALUE(0);
    // mp_obj_str_get_str(method);
    // const char *filename = mp_obj_str_get_str(filename_in);
    // void *data = NULL;
    // size_t len = 0;

    // stat_file("otherfile");

    // printf("Reading a file, about to notify\n");
    // req_file("somfile");
    // printf("Notified\n");

    // MEMZIP_RESULT err = memzip_locate(filename, &data, &len);
    // if (err != MZ_OK)
    // {
    //     return MP_OBJ_NEW_SMALL_INT(1);
    // }

    // return mp_obj_new_bytearray_by_ref(len, data);
}

MP_DEFINE_CONST_FUN_OBJ_1(continuation_storereq_obj, py_continuation_storereq);
// STATIC mp_obj_continuation_t py_continuation_loadreq

STATIC mp_obj_t py_continuation_complete(void)
{
    printf("Completing continuation\n");
    cont_done = 0;
    return mp_const_none;
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_complete_obj, py_continuation_complete);

STATIC const mp_rom_map_elem_t mp_module_continuation_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_continuation)},
    {MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&continuation_info_obj)},
    {MP_ROM_QSTR(MP_QSTR_storereq), MP_ROM_PTR(&continuation_storereq_obj)},
    {MP_ROM_QSTR(MP_QSTR_complete), MP_ROM_PTR(&continuation_complete_obj)},
};

STATIC MP_DEFINE_CONST_DICT(mp_module_continuation_globals, mp_module_continuation_globals_table);

const mp_obj_module_t mp_module_continuation = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mp_module_continuation_globals,
};

MP_REGISTER_MODULE(MP_QSTR_continuation, mp_module_continuation);

// #endif