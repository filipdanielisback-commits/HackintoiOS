#include "../adreno618.h"

#include <assert.h>
#include <stdio.h>

static void test_initial_state(void)
{
    struct adreno618_device device;
    adreno618_device_init(&device);
    assert(device.state == ADRENO618_STATE_DETACHED);
    assert(device.identity.identity_verified == false);
    assert(device.resource.mapping_verified == false);
}

static void test_reject_unverified_identity(void)
{
    struct adreno618_device device;
    const struct adreno618_identity identity = {618U, false};

    adreno618_device_init(&device);
    assert(adreno618_identify(&device, &identity) == ADRENO618_E_IDENTITY);
    assert(device.state == ADRENO618_STATE_DETACHED);
}

static void test_reject_wrong_model(void)
{
    struct adreno618_device device;
    const struct adreno618_identity identity = {642U, true};

    adreno618_device_init(&device);
    assert(adreno618_identify(&device, &identity) == ADRENO618_E_IDENTITY);
}

static void test_require_identity_before_resource(void)
{
    struct adreno618_device device;
    const struct adreno618_resource resource = {
        (uintptr_t)0x1000, 0x1000U, true
    };

    adreno618_device_init(&device);
    assert(adreno618_bind_resource(&device, &resource) == ADRENO618_E_STATE);
}

static void test_complete_verified_binding(void)
{
    struct adreno618_device device;
    const struct adreno618_identity identity = {618U, true};
    const struct adreno618_resource resource = {
        (uintptr_t)0x1000, 0x1000U, true
    };

    adreno618_device_init(&device);
    assert(adreno618_identify(&device, &identity) == ADRENO618_OK);
    assert(device.state == ADRENO618_STATE_IDENTIFIED);
    assert(adreno618_bind_resource(&device, &resource) == ADRENO618_OK);
    assert(device.state == ADRENO618_STATE_RESOURCE_BOUND);
    assert(device.resource.mapped_size == 0x1000U);
    adreno618_detach(&device);
    assert(device.state == ADRENO618_STATE_DETACHED);
}

int main(void)
{
    test_initial_state();
    test_reject_unverified_identity();
    test_reject_wrong_model();
    test_require_identity_before_resource();
    test_complete_verified_binding();
    puts("Adreno 618 core tests passed (host-only; no GPU hardware accessed)");
    return 0;
}
