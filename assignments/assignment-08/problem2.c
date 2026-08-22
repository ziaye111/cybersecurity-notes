/*
  AUTHORS:
     Bjorn De Sutter, Ghent University, https://users.elis.ugent.be/~brdsutte/
     Christian Collberg, University of Arizona

  Test whether an MBA expression always evaluates to the correct value.
*/

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <unistd.h>
#include <stdint.h>

/* Enter your MBA expression here. */
int try(int64_t x, int64_t y, int64_t param_3, int64_t param_4) {
  int64_t originalExpressionValue = x + y;
  /* BEGIN: MBA EXPRESSION <<Don't remove this comment>> */
  int64_t mbaExpressionValue = ...;
  /* END: MBA EXPRESSION <<Don't remove this comment>> */
  return originalExpressionValue == mbaExpressionValue; 
}

int try1(int64_t x, int64_t y, int64_t param_3, int64_t param_4) {
  int64_t originalExpressionValue = x + y;
  /* BEGIN: MBA EXPRESSION <<Don't remove this comment>> */
  int64_t mbaExpressionValue = x - ~y -1;
  /* END: MBA EXPRESSION <<Don't remove this comment>> */
  return originalExpressionValue == mbaExpressionValue; 
}
  
/*
  A T-function is a function from n-bit words to n-bit words that has a single cycle length of 2^n.
  That is, starting from any n-bit value, the T-function is guaranteed
  to produce all the other 2^n−1 n-bit values before starting to repeat
  the values.
  CITE: "Pioneer: Verifying Code Integrity and Enforcing Untampered Code Execution on Legacy Systems."
*/
int64_t tFunction(int64_t x) {
  return x + (x*x | 5) % UINT32_MAX; 
}

void tryOne(int64_t p1, int64_t p2, int64_t p3, int64_t p4) {
  int result = try(p1, p2, p3, p4);
     
  // printf("testing %" PRIx64 " %" PRIx64 " %" PRIx64 " %" PRIx64 "\n", p1, p2, p3, p4);
     if (result != 1) {
         printf("wrong value for %" PRIx64 " %" PRIx64 " %" PRIx64 " %" PRIx64 "\n", p1, p2, p3, p4);
	 exit(1);
      }
}

#define NUMBER_OF_TESTS 100000000

void tryRandom(){
   printf("Trying random values\n");
   int64_t p1 = 1;
   int64_t p2 = 2;
   int64_t p3 = 3;
   int64_t p4 = 4;
   for (int64_t tests=0; tests < NUMBER_OF_TESTS; tests++) {
     p1 = tFunction(p1); 
     p2 = tFunction(p2); 
     p3 = tFunction(p3); 
     p4 = tFunction(p4);

     tryOne(p1, p2, p3, p4);
   }
}

#define MAX_SMALL 256

void trySmall(){
   printf("Trying small values\n");
   int seen_false   = 0;
   int seen_true    = 0;
   int num_false    = 0;
   int num_true     = 0;
   for (int64_t p1 = 0; p1 < MAX_SMALL; p1++) {
      for (int64_t p2 = 0; p2 < MAX_SMALL; p2++) {
         for (int64_t p3 = 0; p3 < MAX_SMALL; p3++) {
            for (int64_t p4 = 0; p4 < MAX_SMALL; p4++) {
               tryOne(p1, p2, p3, p4);
	    }
	 }
      }
   }
}

void tryPower2(){
   printf("Trying power of 2 values\n");
   int pow2 [32];
   int p=2;
   for (int i=0; i<32; i++) {
     pow2[i]=p;
     p *= 2;
   };
   for (int32_t p1 = 0; p1 < 32; p1++) {
      for (int32_t p2 = 0; p2 < 32; p2++) {
         for (int32_t p3 = 0; p3 < 32; p3++) {
            for (int32_t p4 = 0; p4 < 32; p4++) {
               tryOne(pow2[p1], pow2[p2], pow2[p3], pow2[p4]);
	    }
	 }
      }
   }
}

int main(int argc, char ** argv) {
  tryRandom();
  trySmall();
  tryPower2();
}
