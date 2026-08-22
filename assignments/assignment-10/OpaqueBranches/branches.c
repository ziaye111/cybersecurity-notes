#include<stdlib.h>
#include<stdio.h>

int x = 42;

void sometimesTaken(int n) {
  int s = 0;
  int x = 0;
  for(int i=0; i<n; i++) {
    if (x == 0) {
       x++;
    } else {
       x--;
    }
    s += x;
  }
}

void taken(int n) {
  int s = 0;
  for(int i=0; i<n; i++) {
    // The compiler switches this branch condition to
    //    if (x == 42) goto ...
    // So this becomes a taken branch
    if (x != 42) s++;
  }
}

void notTaken(int n) {
  int s = 0;
  for(int i=0; i<n; i++) {
    // The compiler switches this branch condition to
    //    if (x != 42) goto ...
    // So this becomes a not taken branch
    if (x == 42) s++;
  }
}

int main(int argc, char** argv){
  if (argc < 2) abort();
  long numTaken = strtol(argv[1],NULL,10);
  long numNotTaken = strtol(argv[2],NULL,10);
  long numSometimesTaken = strtol(argv[3],NULL,10);

  taken(numTaken);
  notTaken(numNotTaken);
  sometimesTaken(numSometimesTaken);
  return 0;
}
