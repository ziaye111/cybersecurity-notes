#include <stdio.h>
#include <stdlib.h>
#include "pin.H"

void insertCall(.....) {
                     ....
}

void insertRet(.....) {
                     ....
}

VOID Instruction(INS ins, VOID* v) {

      INS_InsertCall(ins, 
                     IPOINT_TAKEN_BRANCH, 
                     AFUNPTR(insertCall), 
                     ....
                     IARG_END);

     INS_InsertCall(ins,
        IPOINT_BEFORE,
                     ....
        IARG_END);
}

VOID Fini(INT32 code, VOID* v) {
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
