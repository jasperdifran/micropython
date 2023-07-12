#include <stdint.h>

// options to control how MicroPython is built

// Use the minimal starting configuration (disables all optional features).
#define MICROPY_CONFIG_ROM_LEVEL (MICROPY_CONFIG_ROM_LEVEL_MINIMUM)

// You can disable the built-in MicroPython compiler by setting the following
// config option to 0.  If you do this then you won't get a REPL prompt, but you
// will still be able to execute pre-compiled scripts, compiled with mpy-cross.
#define MICROPY_ENABLE_COMPILER     (1)

#define MICROPY_QSTR_EXTRA_POOL           mp_qstr_frozen_const_pool
#define MICROPY_ENABLE_GC                 (1)
#define MICROPY_HELPER_REPL               (1)
#define MICROPY_MODULE_FROZEN_MPY         (1)
#define MICROPY_ENABLE_EXTERNAL_IMPORT    (1)
#define MICROPY_MODULE_OVERRIDE_MAIN_IMPORT (1)

#define MICROPY_MODULE_WEAK_LINKS               (1)
#define MICROPY_PY_SYS_EXC_INFO     (1)
// #define MICROPY_COMP_MODULE_CONST               (1)
#define MICROPY_PY_URANDOM                      (1)

#define MICROPY_PY_SYS_PATH_DEFAULT ".frozen:~/.micropython/lib:/usr/lib/micropython"

// Fine control over Python builtins, classes, modules, etc.
#define MICROPY_PY_FSTRINGS                     (1)
#define MICROPY_PY_SYS                         (1)
// #define MICROPY_PY_BUILTINS_BYTES_HEX           (1)
// #define MICROPY_PY_BUILTINS_STR_UNICODE         (1)
// #define MICROPY_PY_BUILTINS_STR_CENTER          (1)
// #define MICROPY_PY_BUILTINS_STR_PARTITION       (1)
// #define MICROPY_PY_BUILTINS_STR_SPLITLINES      (1)
// #define MICROPY_PY_BUILTINS_MEMORYVIEW          (1)
// #define MICROPY_PY_BUILTINS_SLICE_ATTRS         (1)
// #define MICROPY_PY_BUILTINS_SLICE_INDICES       (1)
// #define MICROPY_PY_BUILTINS_FROZENSET           (1)
// #define MICROPY_PY_BUILTINS_ROUND_INT           (1)


#define MICROPY_ALLOC_PATH_MAX            (256 * 16)
#define MICROPY_ALLOC_PARSE_CHUNK_INIT    (64)

// type definitions for the specific machine

typedef intptr_t mp_int_t; // must be pointer size
typedef uintptr_t mp_uint_t; // must be pointer size
typedef long mp_off_t;

// We need to provide a declaration/definition of alloca()
#include <alloca.h>

#define MICROPY_HW_BOARD_NAME "minimal"
#define MICROPY_HW_MCU_NAME "unknown-cpu"

#ifdef __linux__
#define MICROPY_MIN_USE_STDOUT (1)
#endif

#ifdef __thumb__
#define MICROPY_MIN_USE_CORTEX_CPU (1)
#define MICROPY_MIN_USE_STM32_MCU (1)
#endif

#define MP_STATE_PORT MP_STATE_VM