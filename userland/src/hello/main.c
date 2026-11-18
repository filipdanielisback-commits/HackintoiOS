#include <stdio.h>
#include <sys/utsname.h>

int main(void)
{
    struct utsname system_info;

    puts("HackintoiOS userland smoke test");
    puts("This is an original project test program, not an iOS component.");

    if (uname(&system_info) == 0) {
        printf("System: %s\n", system_info.sysname);
        printf("Release: %s\n", system_info.release);
        printf("Machine: %s\n", system_info.machine);
    } else {
        puts("System information is unavailable on this host.");
    }

    return 0;
}
