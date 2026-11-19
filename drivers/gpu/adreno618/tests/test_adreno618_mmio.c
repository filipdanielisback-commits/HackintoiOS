#include "../adreno618_mmio.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

struct fake_mmio {
    uint32_t registers[16];
    bool fail_read;
    bool fail_write;
    unsigned int reads;
    unsigned int writes;
};

static int fake_read32(void *context, uint32_t offset, uint32_t *value)
{
    struct fake_mmio *fake = context;
    if (fake->fail_read || (offset / 4U) >= 16U)
        return -1;
    *value = fake->registers[offset / 4U];
    fake->reads++;
    return 0;
}

static int fake_write32(void *context, uint32_t offset, uint32_t value)
{
    struct fake_mmio *fake = context;
    if (fake->fail_write || (offset / 4U) >= 16U)
        return -1;
    fake->registers[offset / 4U] = value;
    fake->writes++;
    return 0;
}

static const struct adreno618_mmio_ops fake_ops = {
    fake_read32, fake_write32
};

static void test_read_write_and_bounds(void)
{
    struct fake_mmio fake;
    struct adreno618_mmio_window window;
    uint32_t value = 0U;

    memset(&fake, 0, sizeof(fake));
    assert(adreno618_mmio_window_init(&window, &fake_ops, &fake,
        sizeof(fake.registers), true) == ADRENO618_MMIO_OK);
    assert(adreno618_mmio_write32(&window, 0x10U, 0xA618U) ==
        ADRENO618_MMIO_OK);
    assert(adreno618_mmio_read32(&window, 0x10U, &value) ==
        ADRENO618_MMIO_OK);
    assert(value == 0xA618U);
    assert(fake.reads == 1U && fake.writes == 1U);
    assert(adreno618_mmio_read32(&window, 0x3CU, &value) ==
        ADRENO618_MMIO_OK);
    assert(adreno618_mmio_read32(&window, 0x40U, &value) ==
        ADRENO618_MMIO_E_RANGE);
    assert(adreno618_mmio_read32(&window, 0x02U, &value) ==
        ADRENO618_MMIO_E_ALIGNMENT);
}

static void test_read_only_window(void)
{
    struct fake_mmio fake;
    struct adreno618_mmio_window window;

    memset(&fake, 0, sizeof(fake));
    assert(adreno618_mmio_window_init(&window, &fake_ops, &fake,
        sizeof(fake.registers), false) == ADRENO618_MMIO_OK);
    assert(adreno618_mmio_write32(&window, 0U, 1U) ==
        ADRENO618_MMIO_E_READ_ONLY);
    assert(fake.writes == 0U);
}

static void test_callback_failures_and_invalid_setup(void)
{
    struct fake_mmio fake;
    struct adreno618_mmio_window window;
    struct adreno618_mmio_ops read_only_ops = {fake_read32, NULL};
    uint32_t value = 0U;

    memset(&fake, 0, sizeof(fake));
    assert(adreno618_mmio_window_init(&window, &fake_ops, &fake, 3U,
        true) == ADRENO618_MMIO_E_SIZE);
    assert(adreno618_mmio_window_init(&window, &read_only_ops, &fake,
        sizeof(fake.registers), true) == ADRENO618_MMIO_E_ARGUMENT);
    assert(adreno618_mmio_window_init(&window, &fake_ops, &fake,
        sizeof(fake.registers), true) == ADRENO618_MMIO_OK);

    fake.fail_read = true;
    assert(adreno618_mmio_read32(&window, 0U, &value) ==
        ADRENO618_MMIO_E_IO);
    fake.fail_read = false;
    fake.fail_write = true;
    assert(adreno618_mmio_write32(&window, 0U, 1U) ==
        ADRENO618_MMIO_E_IO);
    assert(adreno618_mmio_read32(NULL, 0U, &value) ==
        ADRENO618_MMIO_E_ARGUMENT);
    adreno618_mmio_window_reset(&window);
    assert(adreno618_mmio_read32(&window, 0U, &value) ==
        ADRENO618_MMIO_E_ARGUMENT);
}

int main(void)
{
    test_read_write_and_bounds();
    test_read_only_window();
    test_callback_failures_and_invalid_setup();
    puts("Adreno 618 MMIO interface tests passed (synthetic host backend only)");
    return 0;
}
