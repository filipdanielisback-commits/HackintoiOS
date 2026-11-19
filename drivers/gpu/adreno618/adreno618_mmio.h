#ifndef HACKINTIOS_ADRENO618_MMIO_H
#define HACKINTIOS_ADRENO618_MMIO_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

enum adreno618_mmio_status {
    ADRENO618_MMIO_OK = 0,
    ADRENO618_MMIO_E_ARGUMENT = -60,
    ADRENO618_MMIO_E_SIZE = -61,
    ADRENO618_MMIO_E_ALIGNMENT = -62,
    ADRENO618_MMIO_E_RANGE = -63,
    ADRENO618_MMIO_E_READ_ONLY = -64,
    ADRENO618_MMIO_E_IO = -65
};

/*
 * Platform-owned accessors for an already-mapped resource window.
 * The portable driver never converts physical addresses into pointers.
 * A platform backend is responsible for mapping, ordering, and access policy.
 */
struct adreno618_mmio_ops {
    int (*read32)(void *context, uint32_t offset, uint32_t *value);
    int (*write32)(void *context, uint32_t offset, uint32_t value);
};

struct adreno618_mmio_window {
    struct adreno618_mmio_ops ops;
    void *context;
    size_t size;
    bool initialized;
    bool writable;
};

enum adreno618_mmio_status adreno618_mmio_window_init(
    struct adreno618_mmio_window *window,
    const struct adreno618_mmio_ops *ops,
    void *context,
    size_t mapped_size,
    bool writable);

enum adreno618_mmio_status adreno618_mmio_read32(
    const struct adreno618_mmio_window *window,
    uint32_t offset,
    uint32_t *value);

enum adreno618_mmio_status adreno618_mmio_write32(
    const struct adreno618_mmio_window *window,
    uint32_t offset,
    uint32_t value);

void adreno618_mmio_window_reset(struct adreno618_mmio_window *window);

#ifdef __cplusplus
}
#endif

#endif
