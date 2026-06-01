#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>

/* Forward declaration */
extern "C" void vault_flag();

int main() {
    /* Call vault_flag directly */
    vault_flag();
    return 0;
}
