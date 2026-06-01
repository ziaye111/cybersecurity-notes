# Nodehub Challenge — Learning Summary

This challenge helped me practice binary exploitation, C++ object layout, memory corruption analysis, and debugging with GDB.

## What I practiced

- Reading C++ source code carefully
- Understanding stack and heap behavior
- Inspecting object memory layout in GDB
- Understanding virtual function tables
- Using checksec to analyze binary protections
- Testing local exploitation before remote exploitation
- Writing staged exploit scripts
- Documenting failed attempts and final reasoning

## Important protections observed

- PIE enabled
- NX enabled
- Stack canary enabled
- Full RELRO enabled
- SHSTK / IBT enabled
- Debug symbols available

## Main vulnerability ideas

The analysis focused on unsafe string handling, missing null termination, length confusion, and incorrect memory clearing behavior.

The most important lesson was that exploitation is not only about writing a script. The real work is understanding memory, object layout, control flow, and why each step works.

## Personal note

This challenge was difficult, but it improved my understanding of low-level security, C++ internals, debugging, and exploit development.
