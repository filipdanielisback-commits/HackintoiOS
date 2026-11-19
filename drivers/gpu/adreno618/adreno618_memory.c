#include "adreno618_memory.h"

#include <stdint.h>

static bool is_power_of_two(size_t value)
{
    return value != 0U && (value & (value - 1U)) == 0U;
}

static void clear_view(struct adreno618_memory_view *view)
{
    if (view == NULL)
        return;
    view->data = NULL;
    view->size = 0U;
    view->offset = 0U;
}

enum adreno618_memory_status adreno618_memory_init(
    struct adreno618_memory_object *object,
    void *backing_store,
    size_t size,
    size_t alignment,
    uint32_t access)
{
    uintptr_t address;

    if (object == NULL || backing_store == NULL)
        return ADRENO618_MEMORY_E_ARGUMENT;
    if (size == 0U)
        return ADRENO618_MEMORY_E_SIZE;
    if (!is_power_of_two(alignment))
        return ADRENO618_MEMORY_E_ALIGNMENT;
    if ((access & ~ADRENO618_MEMORY_VALID_FLAGS) != 0U || access == 0U)
        return ADRENO618_MEMORY_E_ACCESS;

    address = (uintptr_t)backing_store;
    if ((address & (uintptr_t)(alignment - 1U)) != 0U)
        return ADRENO618_MEMORY_E_ALIGNMENT;

    object->backing_store = (uint8_t *)backing_store;
    object->size = size;
    object->alignment = alignment;
    object->access = access;
    object->initialized = true;
    object->mapped = false;
    return ADRENO618_MEMORY_OK;
}

enum adreno618_memory_status adreno618_memory_map(
    struct adreno618_memory_object *object,
    size_t offset,
    size_t length,
    uint32_t requested_access,
    struct adreno618_memory_view *view)
{
    if (object == NULL || view == NULL)
        return ADRENO618_MEMORY_E_ARGUMENT;
    clear_view(view);
    if (!object->initialized || object->backing_store == NULL)
        return ADRENO618_MEMORY_E_ARGUMENT;
    if (object->mapped)
        return ADRENO618_MEMORY_E_MAPPED;
    if (length == 0U || offset > object->size ||
        length > object->size - offset)
        return ADRENO618_MEMORY_E_RANGE;
    if (requested_access == 0U ||
        (requested_access & ~ADRENO618_MEMORY_VALID_FLAGS) != 0U ||
        (requested_access & object->access) != requested_access)
        return ADRENO618_MEMORY_E_ACCESS;

    object->mapped = true;
    view->data = object->backing_store + offset;
    view->size = length;
    view->offset = offset;
    return ADRENO618_MEMORY_OK;
}

enum adreno618_memory_status adreno618_memory_unmap(
    struct adreno618_memory_object *object,
    struct adreno618_memory_view *view)
{
    if (object == NULL || view == NULL)
        return ADRENO618_MEMORY_E_ARGUMENT;
    if (!object->initialized || !object->mapped)
        return ADRENO618_MEMORY_E_NOT_MAPPED;

    object->mapped = false;
    clear_view(view);
    return ADRENO618_MEMORY_OK;
}

void adreno618_memory_reset(struct adreno618_memory_object *object)
{
    if (object == NULL)
        return;
    object->backing_store = NULL;
    object->size = 0U;
    object->alignment = 0U;
    object->access = 0U;
    object->initialized = false;
    object->mapped = false;
}
