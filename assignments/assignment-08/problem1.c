/*
  AUTHORS:
     Bjorn De Sutter, Ghent University, https://users.elis.ugent.be/~brdsutte/
     Christian Collberg, University of Arizona

  Test whether an opaque expression always evaluates to a target value.
*/

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <unistd.h>
#include <stdint.h>

/* Enter your opaque expression here. */
uint64_t try(uint64_t param_1, uint64_t param_2, uint64_t param_3, uint64_t param_4) {
  /* BEGIN: TARGET VALUE <<Don't remove this comment>> */
  return 0; 
  /* END: TARGET VALUE <<Don't remove this comment>> */
}

/* Always evaluates to 2. */
uint64_t try2(uint64_t x, uint64_t y, uint64_t param_3, uint64_t param_4) {
  return -(x ^ y) - 2 * ~(x | y) - x - y; 
}
  
/*
  A T-function is a function from n-bit words to n-bit words that has a single cycle length of 2^n.
  That is, starting from any n-bit value, the T-function is guaranteed
  to produce all the other 2^n−1 n-bit values before starting to repeat
  the values.
  CITE: "Pioneer: Verifying Code Integrity and Enforcing Untampered Code Execution on Legacy Systems."
*/
uint64_t tFunction(uint64_t x) {
  return x + (x*x | 5) % UINT32_MAX; 
}

void tryOne(uint64_t p1, uint64_t p2, uint64_t p3, uint64_t p4,
	    int target) {
  int result = try(p1, p2, p3, p4);
     
  // printf("testing %" PRIx64 " %" PRIx64 " %" PRIx64 " %" PRIx64 "\n", p1, p2, p3, p4);
     if (result != target) {
         printf("wrong value for %" PRIx64 " %" PRIx64 " %" PRIx64 " %" PRIx64 "\n", p1, p2, p3, p4);
	 exit(1);
      }
}

#define NUMBER_OF_TESTS 100000000

void tryRandom(int target){
   printf("Trying random values\n");
   uint64_t p1 = 1;
   uint64_t p2 = 2;
   uint64_t p3 = 3;
   uint64_t p4 = 4;
   for (uint64_t tests=0; tests < NUMBER_OF_TESTS; tests++) {
     p1 = tFunction(p1); 
     p2 = tFunction(p2); 
     p3 = tFunction(p3); 
     p4 = tFunction(p4);

     tryOne(p1, p2, p3, p4, target);
   }
}

#define MAX_SMALL 256

void trySmall(int target){
   printf("Trying small values\n");
   int seen_false   = 0;
   int seen_true    = 0;
   int num_false    = 0;
   int num_true     = 0;
   for (uint64_t p1 = 0; p1 < MAX_SMALL; p1++) {
      for (uint64_t p2 = 0; p2 < MAX_SMALL; p2++) {
         for (uint64_t p3 = 0; p3 < MAX_SMALL; p3++) {
            for (uint64_t p4 = 0; p4 < MAX_SMALL; p4++) {
               tryOne(p1, p2, p3, p4, target);
	    }
	 }
      }
   }
}

void tryPower2(int target){
   printf("Trying power of 2 values\n");
   int pow2 [32];
   int p=2;
   for (int i=0; i<32; i++) {
     pow2[i]=p;
     p *= 2;
   };
   for (uint32_t p1 = 0; p1 < 32; p1++) {
      for (uint32_t p2 = 0; p2 < 32; p2++) {
         for (uint32_t p3 = 0; p3 < 32; p3++) {
            for (uint32_t p4 = 0; p4 < 32; p4++) {
               tryOne(pow2[p1], pow2[p2], pow2[p3], pow2[p4], target);
	    }
	 }
      }
   }
}

int main(int argc, char ** argv) {
  int target = 2; /* Set your target value here. */
  tryRandom(target);
  trySmall(target);
  tryPower2(target);
}
