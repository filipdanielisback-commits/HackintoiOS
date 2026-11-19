#include "adreno618.h"

void adreno618_device_init(struct adreno618_device *device)
{
    if (device == NULL)
        return;

    device->state = ADRENO618_STATE_DETACHED;
    device->identity.gpu_model = 0;
    device->identity.identity_verified = false;
    device->resource.mapped_base = (uintptr_t)0;
    device->resource.mapped_size = 0;
    device->resource.mapping_verified = false;
}

enum adreno618_status adreno618_identify(
    struct adreno618_device *device,
    const struct adreno618_identity *identity)
{
    if (device == NULL || identity == NULL)
        return ADRENO618_E_ARGUMENT;
    if (device->state != ADRENO618_STATE_DETACHED)
        return ADRENO618_E_STATE;
    if (!identity->identity_verified || identity->gpu_model != 618U)
        return ADRENO618_E_IDENTITY;

    device->identity = *identity;
    device->state = ADRENO618_STATE_IDENTIFIED;
    return ADRENO618_OK;
}

enum adreno618_status adreno618_bind_resource(
    struct adreno618_device *device,
    const struct adreno618_resource *resource)
{
    if (device == NULL || resource == NULL)
        return ADRENO618_E_ARGUMENT;
    if (device->state != ADRENO618_STATE_IDENTIFIED)
        return ADRENO618_E_STATE;
    if (!resource->mapping_verified ||
        resource->mapped_base == (uintptr_t)0 ||
        resource->mapped_size == 0)
        return ADRENO618_E_RESOURCE;

    device->resource = *resource;
    device->state = ADRENO618_STATE_RESOURCE_BOUND;
    return ADRENO618_OK;
}

void adreno618_detach(struct adreno618_device *device)
{
    adreno618_device_init(device);
}

const char *adreno618_status_string(enum adreno618_status status)
{
    switch (status) {
    case ADRENO618_OK:
        return "ok";
    case ADRENO618_E_ARGUMENT:
        return "invalid argument";
    case ADRENO618_E_IDENTITY:
        return "unverified or non-Adreno-618 identity";
    case ADRENO618_E_RESOURCE:
        return "unverified or empty mapped resource";
    case ADRENO618_E_STATE:
        return "invalid driver state transition";
    default:
        return "unknown status";
    }
}
