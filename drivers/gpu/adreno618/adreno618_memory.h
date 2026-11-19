#ifndef HACKINTIOS_ADRENO618_MEMORY_H
#define HACKINTIOS_ADRENO618_MEMORY_H

#include "adreno618.h"

#ifdef __cplusplus
extern "C" {
#endif

#define ADRENO618_MEMORY_READ  (1U << 0)
#define ADRENO618_MEMORY_WRITE (1U << 1)
#define ADRENO618_MEMORY_VALID_FLAGS (ADRENO618_MEMORY_READ | ADRENO618_MEMORY_WRITE)

enum adreno618_memory_status {
    ADRENO618_MEMORY_OK = 0,
    ADRENO618_MEMORY_E_ARGUMENT = -20,
    ADRENO618_MEMORY_E_SIZE = -21,
    ADRENO618_MEMORY_E_ALIGNMENT = -22,
    ADRENO618_MEMORY_E_ACCESS = -23,
    ADRENO618_MEMORY_E_RANGE = -24,
    ADRENO618_MEMORY_E_MAPPED = -25,
    ADRENO618_MEMORY_E_NOT_MAPPED = -26
};

/*
 * Portable CPU-side buffer descriptor.
 * backing_store is supplied and owned by the caller. This API does not
 * allocate physical pages, create DMA mappings, or expose GPU addresses.
 */
struct adreno618_memory_object {
    uint8_t *backing_store;
    size_t size;
    size_t alignment;
    uint32_t access;
    bool initialized;
    bool mapped;
};

struct adreno618_memory_view {
    uint8_t *data;
    size_t size;
    size_t offset;
};

enum adreno618_memory_status adreno618_memory_init(
    struct adreno618_memory_object *object,
    void *backing_store,
    size_t size,
    size_t alignment,
    uint32_t access);
enum adreno618_memory_status adreno618_memory_map(
    struct adreno618_memory_object *object,
    size_t offset,
    size_t length,
    uint32_t requested_access,
    struct adreno618_memory_view *view);
enum adreno618_memory_status adreno618_memory_unmap(
    struct adreno618_memory_object *object,
    struct adreno618_memory_view *view);
void adreno618_memory_reset(struct adreno618_memory_object *object);

#ifdef __cplusplus
}
#endif

#endif
