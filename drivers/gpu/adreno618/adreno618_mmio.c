#include "adreno618_mmio.h"

#include <string.h>

static enum adreno618_mmio_status validate_offset(
    const struct adreno618_mmio_window *window,
    uint32_t offset)
{
    if (window == NULL || !window->initialized)
        return ADRENO618_MMIO_E_ARGUMENT;
    if ((offset & 3U) != 0U)
        return ADRENO618_MMIO_E_ALIGNMENT;
    if (window->size < sizeof(uint32_t) ||
        (size_t)offset > window->size - sizeof(uint32_t))
        return ADRENO618_MMIO_E_RANGE;
    return ADRENO618_MMIO_OK;
}

enum adreno618_mmio_status adreno618_mmio_window_init(
    struct adreno618_mmio_window *window,
    const struct adreno618_mmio_ops *ops,
    void *context,
    size_t mapped_size,
    bool writable)
{
    if (window == NULL || ops == NULL || ops->read32 == NULL)
        return ADRENO618_MMIO_E_ARGUMENT;
    if (mapped_size < sizeof(uint32_t))
        return ADRENO618_MMIO_E_SIZE;
    if (writable && ops->write32 == NULL)
        return ADRENO618_MMIO_E_ARGUMENT;

    memset(window, 0, sizeof(*window));
    window->ops = *ops;
    window->context = context;
    window->size = mapped_size;
    window->writable = writable;
    window->initialized = true;
    return ADRENO618_MMIO_OK;
}

enum adreno618_mmio_status adreno618_mmio_read32(
    const struct adreno618_mmio_window *window,
    uint32_t offset,
    uint32_t *value)
{
    enum adreno618_mmio_status status;

    if (value == NULL)
        return ADRENO618_MMIO_E_ARGUMENT;
    status = validate_offset(window, offset);
    if (status != ADRENO618_MMIO_OK)
        return status;
    if (window->ops.read32(window->context, offset, value) != 0)
        return ADRENO618_MMIO_E_IO;
    return ADRENO618_MMIO_OK;
}

enum adreno618_mmio_status adreno618_mmio_write32(
    const struct adreno618_mmio_window *window,
    uint32_t offset,
    uint32_t value)
{
    enum adreno618_mmio_status status;

    status = validate_offset(window, offset);
    if (status != ADRENO618_MMIO_OK)
        return status;
    if (!window->writable || window->ops.write32 == NULL)
        return ADRENO618_MMIO_E_READ_ONLY;
    if (window->ops.write32(window->context, offset, value) != 0)
        return ADRENO618_MMIO_E_IO;
    return ADRENO618_MMIO_OK;
}

void adreno618_mmio_window_reset(struct adreno618_mmio_window *window)
{
    if (window != NULL)
        memset(window, 0, sizeof(*window));
}
