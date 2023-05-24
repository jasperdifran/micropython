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

#include "py/builtin.h"
#include "py/runtime.h"
#include "websrvint.h"
#include <stdio.h>
#include <unistd.h>

#include <shared/memzip/memzip.h>

typedef unsigned int sel4cp_channel;
extern void *data;
extern void *private_data;
extern int request_done;
extern int data_len;
extern int status;

STATIC mp_obj_t py_continuation_info(void)
{
    return mp_obj_new_str("Continuation management", 24);
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_info_obj, py_continuation_info);

// STATIC mp_obj_t py_continuation_storereq()
// {
//     void *data = cont_data_store;
// }

/**
 * @brief Expect a JSON string which we can simply copy to private_data. Should be under 4k!
 *
 * @param o_in
 * @return STATIC
 */
STATIC mp_obj_t py_continuation_storeprivatedata(mp_obj_t data)
{
    printf("Storing private data\n");
    private_data_t *priv = (private_data_t *)private_data;
    priv->page_req = mp_obj_get_int(mp_obj_dict_get(data, mp_obj_new_str("page_req", 8)));
    priv->start_time = mp_obj_get_int(mp_obj_dict_get(data, mp_obj_new_str("start_time", 10)));
    priv->addBreadcrumbs = mp_obj_get_int(mp_obj_dict_get(data, mp_obj_new_str("addBreadcrumbs", 14)));

    if (mp_obj_dict_get(data, mp_obj_new_str("file_size", 9)) == mp_const_none)
    {
        priv->file_size = -1;
    }
    else
    {
        priv->file_size = mp_obj_get_int(mp_obj_dict_get(data, mp_obj_new_str("file_size", 9)));
    }
    const char *headers_str = mp_obj_str_get_str(mp_obj_dict_get(data, mp_obj_new_str("headers", 7)));
    const char *method_str = mp_obj_str_get_str(mp_obj_dict_get(data, mp_obj_new_str("method", 6)));
    const char *pagePath_str = mp_obj_str_get_str(mp_obj_dict_get(data, mp_obj_new_str("pagePath", 8)));
    const char *filePath_str = mp_obj_str_get_str(mp_obj_dict_get(data, mp_obj_new_str("filePath", 8)));
    const char *uri_str = mp_obj_str_get_str(mp_obj_dict_get(data, mp_obj_new_str("uri", 3)));
    const char *protocol_str = mp_obj_str_get_str(mp_obj_dict_get(data, mp_obj_new_str("protocol", 8)));

    int headerslen = strlen(headers_str);
    int methodlen = strlen(method_str);
    int pagePathLen = strlen(pagePath_str);
    int filePath = strlen(filePath_str);
    int uriLen = strlen(uri_str);
    int protocolLen = strlen(protocol_str);

    priv->headers = (char *)priv + sizeof(private_data_t);
    strcpy(priv->headers, headers_str);
    priv->headers[headerslen] = '\0';

    priv->method = priv->headers + headerslen + 1;
    strcpy(priv->method, method_str);
    priv->method[methodlen] = '\0';

    priv->pagePath = priv->method + methodlen + 1;
    strcpy(priv->pagePath, pagePath_str);
    priv->pagePath[pagePathLen] = '\0';

    priv->filePath = priv->pagePath + pagePathLen + 1;
    strcpy(priv->filePath, filePath_str);
    priv->filePath[filePath] = '\0';

    priv->uri = priv->filePath + filePath + 1;
    strcpy(priv->uri, uri_str);
    priv->uri[uriLen] = '\0';

    priv->protocol = priv->uri + uriLen + 1;
    strcpy(priv->protocol, protocol_str);
    priv->protocol[protocolLen] = '\0';

    return MP_OBJ_SMALL_INT_VALUE(0);
}
// {
//     // printf("Storing request\n");
//     // strcpy(private_data, mp_obj_str_get_str(o_in));
//     // return MP_OBJ_SMALL_INT_VALUE(0);

//     printf("Storing request\n");
//     const char *method = mp_obj_str_get_str(mp_obj_dict_get(o_in, mp_obj_new_str("method", 6)));
//     if (method == NULL)
//     {
//         printf("Method is null\n");
//     }
//     else
//     {
//         printf("Method is not null\n");
//         printf(method);
//     }
//     const char *path = mp_obj_str_get_str(mp_obj_dict_get(o_in, mp_obj_new_str("path", 4)));
//     if (path == NULL)
//     {
//         printf("Path is null\n");
//     }
//     else
//     {
//         printf("Path is not null\n");
//         printf(path);
//     }

//     printf("\nGot the method and path\n");
//     req_data_t *req = (req_data_t *)private_data;
//     int methodlen = strlen(method);
//     int pathlen = strlen(path);
//     req->method = (char *)req + sizeof(req_data_t);
//     strcpy(req->method, method);
//     req->method[methodlen] = '\0';
//     req->path = req->method + methodlen + 1;
//     strcpy(req->path, path);
//     req->path[pathlen] = '\0';
//     return MP_OBJ_SMALL_INT_VALUE(0);
// }

MP_DEFINE_CONST_FUN_OBJ_1(continuation_storeprivatedata_obj, py_continuation_storeprivatedata);
// STATIC mp_obj_continuation_t py_continuation_loadreq

/**
 * @brief Returns whatever data is sitting in private_data. This is a JSON string.
 *
 * @return STATIC
 */

STATIC mp_obj_t py_continuation_loadprivatedata(void)
{
    private_data_t *priv = (private_data_t *)private_data;
    mp_obj_t newob = mp_obj_new_dict(7);
    mp_obj_dict_store(newob, mp_obj_new_str("page_req", 8), mp_obj_new_int(priv->page_req));
    mp_obj_dict_store(newob, mp_obj_new_str("start_time", 10), mp_obj_new_int(priv->start_time));
    mp_obj_dict_store(newob, mp_obj_new_str("addBreadcrumbs", 14), mp_obj_new_int(priv->addBreadcrumbs));
    mp_obj_dict_store(newob, mp_obj_new_str("headers", 7), mp_obj_new_str(priv->headers, strlen(priv->headers)));
    mp_obj_dict_store(newob, mp_obj_new_str("method", 6), mp_obj_new_str(priv->method, strlen(priv->method)));
    mp_obj_dict_store(newob, mp_obj_new_str("pagePath", 8), mp_obj_new_str(priv->pagePath, strlen(priv->pagePath)));
    mp_obj_dict_store(newob, mp_obj_new_str("filePath", 8), mp_obj_new_str(priv->filePath, strlen(priv->filePath)));
    mp_obj_dict_store(newob, mp_obj_new_str("uri", 3), mp_obj_new_str(priv->uri, strlen(priv->uri)));
    mp_obj_dict_store(newob, mp_obj_new_str("protocol", 8), mp_obj_new_str(priv->protocol, strlen(priv->protocol)));
    return newob;
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_loadprivatedata_obj, py_continuation_loadprivatedata);

STATIC mp_obj_t py_continuation_loaddata(void) {
    printf("Loading data\n");
    return mp_obj_new_bytes(data, data_len);
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_loaddata_obj, py_continuation_loaddata);

STATIC mp_obj_t py_continuation_stat(void)
{
    MEMZIP_FILE_INFO res;
    memcpy(&res, data, sizeof(MEMZIP_FILE_INFO));

    return mp_obj_new_tuple(4, (mp_obj_t[]){
                                   mp_obj_new_int(res.file_size),
                                   mp_obj_new_int(res.last_mod_date),
                                   mp_obj_new_int(res.last_mod_time),
                                   mp_obj_new_int(res.is_dir)});
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_stat_obj, py_continuation_stat);

STATIC mp_obj_t py_continuation_getstatus(void)
{
    printf("GEtting stastus\n");
    return mp_obj_new_int(status);
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_getstatus_obj, py_continuation_getstatus);

STATIC mp_obj_t py_continuation_finish(void)
{
    printf("Completing continuation\n");
    request_done = 1;
    return mp_const_none;
}

MP_DEFINE_CONST_FUN_OBJ_0(continuation_finish_obj, py_continuation_finish);

STATIC const mp_rom_map_elem_t mp_module_continuation_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_continuation)},
    {MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&continuation_info_obj)},
    {MP_ROM_QSTR(MP_QSTR_storeprivatedata), MP_ROM_PTR(&continuation_storeprivatedata_obj)},
    {MP_ROM_QSTR(MP_QSTR_finish), MP_ROM_PTR(&continuation_finish_obj)},
    {MP_ROM_QSTR(MP_QSTR_getstatus), MP_ROM_PTR(&continuation_getstatus_obj)},
    {MP_ROM_QSTR(MP_QSTR_stat), MP_ROM_PTR(&continuation_stat_obj)},
    {MP_ROM_QSTR(MP_QSTR_loadprivatedata), MP_ROM_PTR(&continuation_loadprivatedata_obj)},
    {MP_ROM_QSTR(MP_QSTR_loaddata), MP_ROM_PTR(&continuation_loaddata_obj)},
};

STATIC MP_DEFINE_CONST_DICT(mp_module_continuation_globals, mp_module_continuation_globals_table);

const mp_obj_module_t mp_module_continuation = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mp_module_continuation_globals,
};

MP_REGISTER_MODULE(MP_QSTR_continuation, mp_module_continuation);

// #endif