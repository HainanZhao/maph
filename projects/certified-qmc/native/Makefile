CC ?= cc
CFLAGS ?= -O3 -std=c11 -Wall -Wextra -Wpedantic

BUILD_DIR := ../build/native
TARGETS := $(BUILD_DIR)/direct_modular $(BUILD_DIR)/fftw_plan_audit \
	$(BUILD_DIR)/streaming_pilot

.PHONY: all clean

all: $(TARGETS)

$(BUILD_DIR)/direct_modular: direct_modular.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -D_POSIX_C_SOURCE=200809L $< -o $@

$(BUILD_DIR)/fftw_plan_audit: fftw_plan_audit.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -D_POSIX_C_SOURCE=200809L $< -o $@ -lfftw3 -lm

$(BUILD_DIR)/streaming_pilot: streaming_pilot.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -D_POSIX_C_SOURCE=200809L -fopenmp $< -o $@

clean:
	rm -f $(TARGETS)
