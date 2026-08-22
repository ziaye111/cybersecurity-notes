#include <stdio.h>

/**********************************************************************/
/* An important extension to C is known as "labels as values". Not    */
/* all C-compilers support this extensios: gcc and clang do.          */
/* The expression '&&L' computes the address of the local label 'L'.  */
/* The statement 'goto* expr' is an "indirect jump", i.e. it jumps to */
/* the address held in the variable 'expr'.                           */
/**********************************************************************/

/**********************************************************************/
/* The 'jumps' variable in function foo below is an array of          */
/* addresses of labels within the foo.                                */
/* Change *only* the values in 'jumps' so that the function computes  */
/* the expression '((start+1)*2)/3+2'.                                */
/* Please don't modify any comments below.                            */
/**********************************************************************/

int foo(int start) {
   /* BEGIN JUMP */
   void* jumps[] = {&&lab2, 0x0};
   /* END JUMP */

   int i=0;
   int result=start;
   while (jumps[i] != 0) {
      goto* jumps[i];
      lab1:
           result *= 2; goto end;
      lab2:
           result /= 3; goto end;
      lab3:
           result += 1; goto end;
      end:
         i++;
   }
   return result;
}

void test(char test, int start) {
   printf("TEST %c: %d\n", test, foo(start));
}

/* BEGIN MAIN */
int main() {
   test('A', 0);
   test('B', 1);
   test('C', 2);
   test('D', 100);
}
/* END MAIN */


