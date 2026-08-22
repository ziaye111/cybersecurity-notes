#include <stdio.h>
#include <stdlib.h>
#include "pin.H"

VOID count_taken(void* addr, int taken) {
   ....

}

VOID Instruction(INS ins, VOID* v) {
         INS_InsertCall(ins, IPOINT_BEFORE, 
                          (AFUNPTR)count_taken, 
                          IARG_INST_PTR, 
                          IARG_BRANCH_TAKEN, 
                          IARG_END);
}

VOID Fini(INT32 code, VOID* v) {
   ..........
}

INT32 Usage() {
    return -1;
}

int main(int argc, char* argv[]) {
    if (PIN_Init(argc, argv)) return Usage();
    INS_AddInstrumentFunction(Instruction, 0);
    PIN_AddFiniFunction(Fini, 0);
    PIN_StartProgram();
    return 0;
}
