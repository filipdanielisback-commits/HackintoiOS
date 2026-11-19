#ifndef HACKINTIOS_ADRENO618_ALLOCATOR_H
#define HACKINTIOS_ADRENO618_ALLOCATOR_H

#include "adreno618_memory.h"

#ifdef __cplusplus
extern "C" {
#endif

enum adreno618_allocator_status {
    ADRENO618_ALLOCATOR_OK = 0,
    ADRENO618_ALLOCATOR_E_ARGUMENT = -40,
    ADRENO618_ALLOCATOR_E_SIZE = -41,
    ADRENO618_ALLOCATOR_E_ALIGNMENT = -42,
    ADRENO618_ALLOCATOR_E_ACCESS = -43,
    ADRENO618_ALLOCATOR_E_RANGE = -44,
    ADRENO618_ALLOCATOR_E_STATE = -45,
    ADRENO618_ALLOCATOR_E_PLATFORM = -46
};

/*
 * Platform callbacks own allocation policy and backing storage. Handles are
 * opaque. No physical, DMA, or GPU virtual address is returned by this API.
 * allocate must honor requested alignment and size or return failure.
 */
struct adreno618_allocator_ops {
    int (*allocate)(void *context, size_t size, size_t alignment, void **handle);
    int (*release)(void *context, void *handle);
    int (*map_cpu)(void *context, void *handle, size_t offset, size_t length,
                   uint32_t access, void **cpu_address);
    int (*unmap_cpu)(void *context, void *handle, void *cpu_address,
                     size_t offset, size_t length, uint32_t access);
};

struct adreno618_allocation {
    struct adreno618_allocator_ops ops;
    void *context;
    void *handle;
    size_t size;
    size_t alignment;
    uint32_t access;
    bool initialized;
    bool mapped;
    void *mapped_address;
    size_t mapped_offset;
    size_t mapped_length;
    uint32_t mapped_access;
};

struct adreno618_allocation_view {
    void *data;
    size_t size;
    size_t offset;
};

void adreno618_allocation_init(struct adreno618_allocation *allocation);
enum adreno618_allocator_status adreno618_allocation_create(
    struct adreno618_allocation *allocation,
    const struct adreno618_allocator_ops *ops, void *context,
    size_t size, size_t alignment, uint32_t access);
enum adreno618_allocator_status adreno618_allocation_map(
    struct adreno618_allocation *allocation, size_t offset, size_t length,
    uint32_t access, struct adreno618_allocation_view *view);
enum adreno618_allocator_status adreno618_allocation_unmap(
    struct adreno618_allocation *allocation,
    struct adreno618_allocation_view *view);
enum adreno618_allocator_status adreno618_allocation_destroy(
    struct adreno618_allocation *allocation);

#ifdef __cplusplus
}
#endif

#endif
