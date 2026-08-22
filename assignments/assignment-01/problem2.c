#include <stdint.h>
#include <stdio.h>

uint32_t foo (uint32_t a, uint32_t b) {
   uint32_t r=0;
   for (int i=0; i<32; i++) {
      r = r | ((((a >> i) & 1) != ((b >> i) & 1)) << i);
   }
   return r;
}

/**********************************************************************/
/* Write a one-line function bar that is equivalent to foo.           */
/* Please don't modify any comments below.                            */
/**********************************************************************/

/* BEGIN BAR */
uint32_t bar (uint32_t a, uint32_t b) {
   return 0;
}
/* END BAR */

void test(char test, uint32_t a, uint32_t b) {
   uint32_t c1 = foo(a, b);
   uint32_t c2 = bar(a, b);
   printf("TEST %c: %i\n", test, c1 == c2);
}

/* BEGIN MAIN */
int main() {
   test('A', 0x0, 0x0);
   test('B', 0xffffffff, 0xffffffff);
   test('C', 0x0, 0xffffffff);
   test('D', 0xffffffff, 0x0);
   test('E', 0xaabbccdd, 0x11223344);
}
/* END MAIN */

