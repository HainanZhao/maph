CC ?= cc
PRODUCTION_CFLAGS := -O3 -std=c11 -Wall -Wextra -Wpedantic \
	-D_POSIX_C_SOURCE=200809L

BUILD_DIR := ../build/production
TARGET := $(BUILD_DIR)/production_prime

.PHONY: all clean

all: $(TARGET)

$(TARGET): ../native/production_prime.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(PRODUCTION_CFLAGS) $< -o $@

clean:
	rm -f $(TARGET)
