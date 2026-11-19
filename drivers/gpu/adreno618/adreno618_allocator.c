#include "adreno618_allocator.h"

#include <stdint.h>
#include <string.h>

static bool valid_alignment(size_t value)
{
    return value != 0U && (value & (value - 1U)) == 0U;
}

static void clear_view(struct adreno618_allocation_view *view)
{
    if (view == NULL)
        return;
    view->data = NULL;
    view->size = 0U;
    view->offset = 0U;
}

static void clear_allocation(struct adreno618_allocation *allocation)
{
    memset(allocation, 0, sizeof(*allocation));
}

enum adreno618_allocator_status adreno618_allocation_create(
    struct adreno618_allocation *allocation,
    const struct adreno618_allocator_ops *ops, void *context,
    size_t size, size_t alignment, uint32_t access)
{
    void *handle = NULL;

    if (allocation == NULL || ops == NULL || ops->allocate == NULL ||
        ops->release == NULL || ops->map_cpu == NULL ||
        ops->unmap_cpu == NULL)
        return ADRENO618_ALLOCATOR_E_ARGUMENT;
    if (allocation->initialized)
        return ADRENO618_ALLOCATOR_E_STATE;
    if (size == 0U)
        return ADRENO618_ALLOCATOR_E_SIZE;
    if (!valid_alignment(alignment))
        return ADRENO618_ALLOCATOR_E_ALIGNMENT;
    if (access == 0U ||
        (access & ~ADRENO618_MEMORY_VALID_FLAGS) != 0U)
        return ADRENO618_ALLOCATOR_E_ACCESS;
    if (ops->allocate(context, size, alignment, &handle) != 0 ||
        handle == NULL)
        return ADRENO618_ALLOCATOR_E_PLATFORM;

    allocation->ops = *ops;
    allocation->context = context;
    allocation->handle = handle;
    allocation->size = size;
    allocation->alignment = alignment;
    allocation->access = access;
    allocation->initialized = true;
    allocation->mapped = false;
    allocation->mapped_address = NULL;
    allocation->mapped_offset = 0U;
    allocation->mapped_length = 0U;
    allocation->mapped_access = 0U;
    return ADRENO618_ALLOCATOR_OK;
}

enum adreno618_allocator_status adreno618_allocation_map(
    struct adreno618_allocation *allocation, size_t offset, size_t length,
    uint32_t access, struct adreno618_allocation_view *view)
{
    void *address = NULL;

    if (allocation == NULL || view == NULL)
        return ADRENO618_ALLOCATOR_E_ARGUMENT;
    clear_view(view);
    if (!allocation->initialized || allocation->handle == NULL)
        return ADRENO618_ALLOCATOR_E_STATE;
    if (allocation->mapped)
        return ADRENO618_ALLOCATOR_E_STATE;
    if (length == 0U || offset > allocation->size ||
        length > allocation->size - offset)
        return ADRENO618_ALLOCATOR_E_RANGE;
    if (access == 0U || (access & ~ADRENO618_MEMORY_VALID_FLAGS) != 0U ||
        (access & allocation->access) != access)
        return ADRENO618_ALLOCATOR_E_ACCESS;
    if (allocation->ops.map_cpu(allocation->context, allocation->handle,
            offset, length, access, &address) != 0 || address == NULL)
        return ADRENO618_ALLOCATOR_E_PLATFORM;

    allocation->mapped = true;
    allocation->mapped_address = address;
    allocation->mapped_offset = offset;
    allocation->mapped_length = length;
    allocation->mapped_access = access;
    view->data = address;
    view->size = length;
    view->offset = offset;
    return ADRENO618_ALLOCATOR_OK;
}

enum adreno618_allocator_status adreno618_allocation_unmap(
    struct adreno618_allocation *allocation,
    struct adreno618_allocation_view *view)
{
    if (allocation == NULL || view == NULL)
        return ADRENO618_ALLOCATOR_E_ARGUMENT;
    if (!allocation->initialized || !allocation->mapped)
        return ADRENO618_ALLOCATOR_E_STATE;
    if (allocation->ops.unmap_cpu(allocation->context, allocation->handle,
            allocation->mapped_address, allocation->mapped_offset,
            allocation->mapped_length, allocation->mapped_access) != 0)
        return ADRENO618_ALLOCATOR_E_PLATFORM;

    allocation->mapped = false;
    allocation->mapped_address = NULL;
    allocation->mapped_offset = 0U;
    allocation->mapped_length = 0U;
    allocation->mapped_access = 0U;
    clear_view(view);
    return ADRENO618_ALLOCATOR_OK;
}

enum adreno618_allocator_status adreno618_allocation_destroy(
    struct adreno618_allocation *allocation)
{
    if (allocation == NULL)
        return ADRENO618_ALLOCATOR_E_ARGUMENT;
    if (!allocation->initialized || allocation->handle == NULL)
        return ADRENO618_ALLOCATOR_E_STATE;
    if (allocation->mapped)
        return ADRENO618_ALLOCATOR_E_STATE;
    if (allocation->ops.release(allocation->context, allocation->handle) != 0)
        return ADRENO618_ALLOCATOR_E_PLATFORM;
    clear_allocation(allocation);
    return ADRENO618_ALLOCATOR_OK;
}
