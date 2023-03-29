include ../../py/mkenv.mk

CROSS = 0

# qstr definitions (must come before including py.mk)
QSTR_DEFS = qstrdefsport.h

# MicroPython feature configurations
MICROPY_ROM_TEXT_COMPRESSION ?= 1

# include py core make definitions
include $(TOP)/py/py.mk

ifeq ($(CROSS), 1)
CROSS_COMPILE ?= aarch64-none-elf-
endif

INC += -I.
INC += -I$(TOP)
INC += -I$(BUILD)
INC += -Iinclude

ifeq ($(CROSS), 1)
DFU = $(TOP)/tools/dfu.py
PYDFU = $(TOP)/tools/pydfu.py
# CFLAGS_CORTEX_M4 = -mthumb -mtune=cortex-m4 -mcpu=cortex-m4 -msoft-float -fsingle-precision-constant -Wdouble-promotion -Wfloat-conversion
CFLAGS = $(INC) -Wall -Werror -std=c99 -fPIC -nostdlib $(COPT) #$(CFLAGS_CORTEX_M4)
LDFLAGS = -nostdlib -r #-fPIC # -shared -ffreestanding 
else
LD = gcc
CFLAGS = $(INC)  -Wall -Werror -Wdouble-promotion -Wfloat-conversion -std=c99 $(COPT)
LDFLAGS = -Wl,-Map=$@.map,--cref -Wl,--gc-sections,-shared,-ffreestanding
endif

CSUPEROPT = -Os # save some code space

# Tune for Debugging or Optimization
CFLAGS += -g  # always include debug info in the ELF
ifeq ($(DEBUG), 1)
CFLAGS += -O0
else
CFLAGS += -Os -DNDEBUG
CFLAGS += -fdata-sections -ffunction-sections
endif

# Flags for optional C++ source code
CXXFLAGS += $(filter-out -std=c99,$(CFLAGS))
CXXFLAGS += $(CXXFLAGS_MOD)

# Flags for user C modules
CFLAGS += $(CFLAGS_MOD)
LDFLAGS += $(LDFLAGS_MOD)

LIBS =

SRC_C = \
	main.c \
	uart_core.c \
	shared/libc/printf.c \
	shared/readline/readline.c \
	shared/runtime/pyexec.c \
	shared/runtime/stdout_helpers.c \
	modcptxrx.c \
	modcpfs.c \
	modutime.c \
	modcontinuation.c \

SRC_C += \
    shared/memzip/import.c \
    shared/memzip/lexermemzip.c \
    shared/memzip/memzip.c \

ifeq ($(CROSS), 1)
SRC_C += shared/libc/string0.c
endif

SRC_C += $(SRC_MOD)

SRC_CXX += $(SRC_MOD_CXX)

SRC_QSTR += shared/readline/readline.c shared/runtime/pyexec.c modcptxrx.c modcpfs.c modutime.c modcontinuation.c
SRC_QSTR += $(SRC_MOD) $(SRC_MOD_CXX)

OBJ += $(BUILD)/memzip-files.o

OBJ += $(PY_CORE_O) $(addprefix $(BUILD)/, $(SRC_C:.c=.o))
OBJ += $(addprefix $(BUILD)/, $(SRC_CXX:.cpp=.o))

MEMZIP_DIR := ./subfiles

MAKE_MEMZIP = ../../shared/memzip/make-memzip.py

all: $(BUILD)/websrv.o

$(BUILD)/memzip-files.o: $(BUILD)/memzip-files.c
    $(call compile_c)

$(BUILD)/memzip-files.c: $(shell find ${MEMZIP_DIR} -type f)
	$(ECHO) "Creating $@"
	$(Q)$(PYTHON) $(MAKE_MEMZIP) --zip-file $(BUILD)/memzip-files.zip --c-file $@ $(MEMZIP_DIR)

$(BUILD)/websrv.o: $(OBJ)
	$(ECHO) "LINK $@"
	$(ECHO) "LIBS $(LIBS), LDFLAGS $(LDFLAGS)"
	$(ECHO) "OBJ $(OBJ)"
	$(Q)$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)
	$(Q)$(SIZE) $@

# Run emulation build on a POSIX system with suitable terminal settings
run:
	@saved_=`stty -g`; \
	  stty raw opost -echo; \
	  $(BUILD)/websrv.elf; \
	  echo "Exit status: $$?"; \
	  stty $$saved_

include $(TOP)/py/mkrules.mk
