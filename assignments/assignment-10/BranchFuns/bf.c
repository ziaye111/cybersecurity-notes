#include<stdio.h>

void notBF (unsigned long offset ) {
    printf("This is a regular old function call\n");
}

void bf (unsigned long offset ) {
  __asm__ volatile ("movq  %0, 8(%%rbp)": : "r" (offset));
}

int main() {
   notBF(42);

   bf((unsigned long)&&L);
   printf("This should never execute\n");
L:
   printf("This should execute\n");
}
