
#include <stdint.h>
#include <stdio.h>

/**********************************************************************/
/* A C union is like a struct, except the fields overlap. So in the   */
/* union convert, below, i and c are at the same location in memory.  */
/**********************************************************************/

union convert {
   uint32_t i;
   char c[4];
};

/**********************************************************************/
/* The function rotateLeft(i) should use convert to split up i into   */
/* its consistent 4 bytes and rotate them one step to the left.      */
/* So, for example,                                                   */
/*    rotateLeft(0xaabbccdd)                                          */
/* should return                                                      */
/*    0xbbccddaa                                                      */
/* Please don't modify any comments below.                            */
/**********************************************************************/

/* BEGIN ROTATE */
uint32_t rotateLeft (int i) {
   union convert x;
   return 0;
}
/* END ROTATE */


/* BEGIN MAIN */
int main () {
   uint32_t x = 0xAABBCCDD;
   printf("%x\n", x);
   x = rotateLeft(x);
   printf("%x\n", x);
   x = rotateLeft(x);
   printf("%x\n", x);
   x = rotateLeft(x);
   printf("%x\n", x);
   x = rotateLeft(x);
   printf("%x\n", x);
}
/* END MAIN */

The function rotateLeft(i) should use convert to split up i into its consistuent 4 bytes and rotate them one step to the left.      
So, for example,                                                   
   rotateLeft(0xaabbccdd)                                          
should return                                                      
   0xbbccddaa                                                      
Please don't modify any comments below.                            
