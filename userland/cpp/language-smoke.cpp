#include <cstdint>

extern "C" std::uint32_t hackintoios_cpp_language_smoke() {
    return 18'712U;
}

int main() {
    return hackintoios_cpp_language_smoke() == 18'712U ? 0 : 1;
}
