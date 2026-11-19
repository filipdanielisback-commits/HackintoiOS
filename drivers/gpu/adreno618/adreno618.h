#ifndef HACKINTIOS_ADRENO618_H
#define HACKINTIOS_ADRENO618_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Early, platform-independent Adreno 618 driver core.
 *
 * This layer deliberately performs no MMIO, firmware loading, clock changes,
 * power sequencing, or command submission. A platform layer must supply
 * independently verified identity and mapped-resource information.
 */

enum adreno618_status {
    ADRENO618_OK = 0,
    ADRENO618_E_ARGUMENT = -1,
    ADRENO618_E_IDENTITY = -2,
    ADRENO618_E_RESOURCE = -3,
    ADRENO618_E_STATE = -4
};

enum adreno618_state {
    ADRENO618_STATE_DETACHED = 0,
    ADRENO618_STATE_IDENTIFIED = 1,
    ADRENO618_STATE_RESOURCE_BOUND = 2
};

struct adreno618_identity {
    uint32_t gpu_model;
    bool identity_verified;
};

struct adreno618_resource {
    uintptr_t mapped_base;
    size_t mapped_size;
    bool mapping_verified;
};

struct adreno618_device {
    enum adreno618_state state;
    struct adreno618_identity identity;
    struct adreno618_resource resource;
};

void adreno618_device_init(struct adreno618_device *device);
enum adreno618_status adreno618_identify(
    struct adreno618_device *device,
    const struct adreno618_identity *identity);
enum adreno618_status adreno618_bind_resource(
    struct adreno618_device *device,
    const struct adreno618_resource *resource);
void adreno618_detach(struct adreno618_device *device);
const char *adreno618_status_string(enum adreno618_status status);

#ifdef __cplusplus
}
#endif

#endif
