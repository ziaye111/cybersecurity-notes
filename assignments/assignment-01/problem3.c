#include <stdint.h>
#include <stdio.h>

/************************************************************************/
/* Write a routine that copies the even-numbered bits from a variable a */
/* into the corresponding bits in variable b. Use only bit-manipulation */
/* instructions. Don't use a loop.                                      */
/* In other words, replace bits 0 (least significant),2,4,...,30 (most  */
/* significant) of b with bits 0,2,4,...,30 from a.                     */
/************************************************************************/

/* BEGIN FOO */
uint32_t foo(uint32_t a, uint32_t b) {
   return 0; 
}
/* END FOO */

void test(char test, uint32_t a, uint32_t b) {
   printf("TEST %c: 0x%x\n", test, foo(a,b));   
}

/* BEGIN MAIN */
int main() {
   test('A', 0x0, 0x0);
   test('B', 0xffffffff, 0xffffffff);
   test('C', 0x0, 0xffffffff);
   test('D', 0xaaaaaaaa, 0x55555555);
   test('E', 0x55555555, 0x0);
   test('F', 0x55555555, 0xaaaaaaaa);
}
/* END MAIN */
