#include "../adreno618_memory.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

static void test_init_and_map(void)
{
    _Alignas(64) uint8_t storage[256] = {0};
    struct adreno618_memory_object object = {0};
    struct adreno618_memory_view view = {0};

    assert(adreno618_memory_init(&object, storage, sizeof(storage), 64U,
        ADRENO618_MEMORY_READ | ADRENO618_MEMORY_WRITE) == ADRENO618_MEMORY_OK);
    assert(adreno618_memory_map(&object, 16U, 32U, ADRENO618_MEMORY_WRITE,
        &view) == ADRENO618_MEMORY_OK);
    assert(view.data == storage + 16U);
    assert(view.size == 32U);
    assert(view.offset == 16U);
    view.data[0] = 0x5aU;
    assert(storage[16] == 0x5aU);
    assert(adreno618_memory_unmap(&object, &view) == ADRENO618_MEMORY_OK);
    assert(view.data == NULL && view.size == 0U);
}

static void test_reject_bad_alignment(void)
{
    _Alignas(64) uint8_t storage[128] = {0};
    struct adreno618_memory_object object = {0};

    assert(adreno618_memory_init(&object, storage + 1U, 64U, 64U,
        ADRENO618_MEMORY_READ) == ADRENO618_MEMORY_E_ALIGNMENT);
    assert(adreno618_memory_init(&object, storage, 64U, 3U,
        ADRENO618_MEMORY_READ) == ADRENO618_MEMORY_E_ALIGNMENT);
}

static void test_reject_invalid_ranges(void)
{
    _Alignas(16) uint8_t storage[64] = {0};
    struct adreno618_memory_object object = {0};
    struct adreno618_memory_view view = {0};

    assert(adreno618_memory_init(&object, storage, sizeof(storage), 16U,
        ADRENO618_MEMORY_READ) == ADRENO618_MEMORY_OK);
    assert(adreno618_memory_map(&object, 60U, 8U, ADRENO618_MEMORY_READ,
        &view) == ADRENO618_MEMORY_E_RANGE);
    assert(adreno618_memory_map(&object, 0U, 0U, ADRENO618_MEMORY_READ,
        &view) == ADRENO618_MEMORY_E_RANGE);
}

static void test_access_and_single_mapping(void)
{
    _Alignas(16) uint8_t storage[64] = {0};
    struct adreno618_memory_object object = {0};
    struct adreno618_memory_view first = {0};
    struct adreno618_memory_view second = {0};

    assert(adreno618_memory_init(&object, storage, sizeof(storage), 16U,
        ADRENO618_MEMORY_READ) == ADRENO618_MEMORY_OK);
    assert(adreno618_memory_map(&object, 0U, 16U, ADRENO618_MEMORY_WRITE,
        &first) == ADRENO618_MEMORY_E_ACCESS);
    assert(adreno618_memory_map(&object, 0U, 16U, ADRENO618_MEMORY_READ,
        &first) == ADRENO618_MEMORY_OK);
    assert(adreno618_memory_map(&object, 16U, 16U, ADRENO618_MEMORY_READ,
        &second) == ADRENO618_MEMORY_E_MAPPED);
    assert(adreno618_memory_unmap(&object, &first) == ADRENO618_MEMORY_OK);
}

static void test_reset(void)
{
    _Alignas(16) uint8_t storage[64] = {0};
    struct adreno618_memory_object object = {0};

    assert(adreno618_memory_init(&object, storage, sizeof(storage), 16U,
        ADRENO618_MEMORY_READ) == ADRENO618_MEMORY_OK);
    adreno618_memory_reset(&object);
    assert(!object.initialized);
    assert(!object.mapped);
    assert(object.backing_store == NULL);
}

int main(void)
{
    test_init_and_map();
    test_reject_bad_alignment();
    test_reject_invalid_ranges();
    test_access_and_single_mapping();
    test_reset();
    puts("Adreno 618 memory-object tests passed (host-only; no DMA/GPU access)");
    return 0;
}
