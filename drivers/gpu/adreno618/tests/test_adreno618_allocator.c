#include "../adreno618_allocator.h"

#include <assert.h>
#include <stdio.h>
#include <stdint.h>

struct fake_platform {
    _Alignas(64) uint8_t storage[256];
    bool fail_allocate;
    bool fail_map;
    bool fail_unmap;
    bool fail_release;
    size_t requested_size;
    size_t requested_alignment;
    unsigned int release_count;
};

static int fake_allocate(void *context, size_t size, size_t alignment,
                         void **handle)
{
    struct fake_platform *platform = context;
    uintptr_t address = (uintptr_t)platform->storage;
    platform->requested_size = size;
    platform->requested_alignment = alignment;
    if (platform->fail_allocate || size > sizeof(platform->storage) ||
        (address & (uintptr_t)(alignment - 1U)) != 0U)
        return -1;
    *handle = platform->storage;
    return 0;
}

static int fake_release(void *context, void *handle)
{
    struct fake_platform *platform = context;
    if (platform->fail_release || handle != platform->storage)
        return -1;
    platform->release_count++;
    return 0;
}

static int fake_map(void *context, void *handle, size_t offset, size_t length,
                    uint32_t access, void **cpu_address)
{
    struct fake_platform *platform = context;
    (void)access;
    if (platform->fail_map || handle != platform->storage ||
        offset > sizeof(platform->storage) ||
        length > sizeof(platform->storage) - offset)
        return -1;
    *cpu_address = platform->storage + offset;
    return 0;
}

static int fake_unmap(void *context, void *handle, void *cpu_address,
                      size_t offset, size_t length, uint32_t access)
{
    struct fake_platform *platform = context;
    (void)length;
    (void)access;
    if (platform->fail_unmap || handle != platform->storage ||
        cpu_address != platform->storage + offset)
        return -1;
    return 0;
}

static const struct adreno618_allocator_ops fake_ops = {
    fake_allocate, fake_release, fake_map, fake_unmap
};

static void test_create_map_unmap_destroy(void)
{
    struct fake_platform platform = {0};
    struct adreno618_allocation allocation;
    struct adreno618_allocation_view view = {0};

    adreno618_allocation_init(&allocation);
    assert(adreno618_allocation_create(&allocation, &fake_ops, &platform,
        128U, 64U, ADRENO618_MEMORY_READ | ADRENO618_MEMORY_WRITE) ==
        ADRENO618_ALLOCATOR_OK);
    assert(platform.requested_size == 128U);
    assert(platform.requested_alignment == 64U);
    assert(adreno618_allocation_map(&allocation, 16U, 32U,
        ADRENO618_MEMORY_WRITE, &view) == ADRENO618_ALLOCATOR_OK);
    assert(view.data == platform.storage + 16U);
    assert(view.size == 32U && view.offset == 16U);
    assert(adreno618_allocation_unmap(&allocation, &view) ==
        ADRENO618_ALLOCATOR_OK);
    assert(view.data == NULL && view.size == 0U);
    assert(adreno618_allocation_destroy(&allocation) ==
        ADRENO618_ALLOCATOR_OK);
    assert(platform.release_count == 1U);
    assert(!allocation.initialized);
}

static void test_allocation_failures_and_validation(void)
{
    struct fake_platform platform = {0};
    struct adreno618_allocation allocation = {0};

    platform.fail_allocate = true;
    assert(adreno618_allocation_create(&allocation, &fake_ops, &platform,
        64U, 16U, ADRENO618_MEMORY_READ) == ADRENO618_ALLOCATOR_E_PLATFORM);
    platform.fail_allocate = false;
    assert(adreno618_allocation_create(&allocation, &fake_ops, &platform,
        0U, 16U, ADRENO618_MEMORY_READ) == ADRENO618_ALLOCATOR_E_SIZE);
    assert(adreno618_allocation_create(&allocation, &fake_ops, &platform,
        64U, 3U, ADRENO618_MEMORY_READ) ==
        ADRENO618_ALLOCATOR_E_ALIGNMENT);
    assert(adreno618_allocation_create(&allocation, &fake_ops, &platform,
        64U, 16U, 0U) == ADRENO618_ALLOCATOR_E_ACCESS);
}

static void test_mapping_failure_and_bounds(void)
{
    struct fake_platform platform = {0};
    struct adreno618_allocation allocation = {0};
    struct adreno618_allocation_view view = {0};

    adreno618_allocation_init(&allocation);
    assert(adreno618_allocation_create(&allocation, &fake_ops, &platform,
        128U, 16U, ADRENO618_MEMORY_READ) == ADRENO618_ALLOCATOR_OK);
    assert(adreno618_allocation_map(&allocation, 120U, 16U,
        ADRENO618_MEMORY_READ, &view) == ADRENO618_ALLOCATOR_E_RANGE);
    assert(adreno618_allocation_map(&allocation, 0U, 8U,
        ADRENO618_MEMORY_WRITE, &view) == ADRENO618_ALLOCATOR_E_ACCESS);
    platform.fail_map = true;
    assert(adreno618_allocation_map(&allocation, 0U, 8U,
        ADRENO618_MEMORY_READ, &view) == ADRENO618_ALLOCATOR_E_PLATFORM);
    assert(!allocation.mapped);
    platform.fail_map = false;
    assert(adreno618_allocation_map(&allocation, 0U, 8U,
        ADRENO618_MEMORY_READ, &view) == ADRENO618_ALLOCATOR_OK);
    assert(adreno618_allocation_destroy(&allocation) ==
        ADRENO618_ALLOCATOR_E_STATE);
    platform.fail_unmap = true;
    assert(adreno618_allocation_unmap(&allocation, &view) ==
        ADRENO618_ALLOCATOR_E_PLATFORM);
    assert(allocation.mapped);
    platform.fail_unmap = false;
    assert(adreno618_allocation_unmap(&allocation, &view) ==
        ADRENO618_ALLOCATOR_OK);
    platform.fail_release = true;
    assert(adreno618_allocation_destroy(&allocation) ==
        ADRENO618_ALLOCATOR_E_PLATFORM);
    assert(allocation.initialized);
    platform.fail_release = false;
    assert(adreno618_allocation_destroy(&allocation) ==
        ADRENO618_ALLOCATOR_OK);
}

int main(void)
{
    test_create_map_unmap_destroy();
    test_allocation_failures_and_validation();
    test_mapping_failure_and_bounds();
    puts("Adreno 618 allocator tests passed (synthetic host platform only)");
    return 0;
}
