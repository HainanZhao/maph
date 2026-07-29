CC ?= cc
RELEASE_CFLAGS := -O3 -std=c11 -Wall -Wextra -Wpedantic \
	-D_POSIX_C_SOURCE=200809L

BUILD_DIR := ../build/native
TARGETS := $(BUILD_DIR)/direct_modular $(BUILD_DIR)/streaming_pilot \
	$(BUILD_DIR)/cycle009_ntt
LEGACY_NUMERICAL_TARGET := $(BUILD_DIR)/fftw_plan_audit

.PHONY: all release clean

all: release

release: $(TARGETS)

$(BUILD_DIR)/direct_modular: direct_modular.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(RELEASE_CFLAGS) $< -o $@

$(BUILD_DIR)/streaming_pilot: streaming_pilot.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(RELEASE_CFLAGS) -fopenmp $< -o $@

$(BUILD_DIR)/cycle009_ntt: cycle009_ntt.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(RELEASE_CFLAGS) $< -o $@

clean:
	rm -f $(TARGETS) $(LEGACY_NUMERICAL_TARGET)
