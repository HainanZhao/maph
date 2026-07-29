CC ?= cc
CFLAGS ?= -O3 -std=c11 -Wall -Wextra -Wpedantic

BUILD_DIR := ../../build/numerical-crosscheck
TARGET := $(BUILD_DIR)/fftw_plan_audit

.PHONY: all clean

all: $(TARGET)

$(TARGET): native/fftw_plan_audit.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -D_POSIX_C_SOURCE=200809L $< -o $@ -lfftw3 -lm

clean:
	rm -f $(TARGET)
