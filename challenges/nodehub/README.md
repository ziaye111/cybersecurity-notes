# Nodehub Challenge Solution

## Overview

Nodehub is a remote IoT management system and it contains several vulnerabilities which can be chained together for exploitation.

The challenge was divided into 2 stages basically:

* Stage 1 → trigger `vault_flag()` and print the first flag
* Stage 2 → achieve code execution and run the `grade` command

At first the binary looked very protected and annoying because it had PIE, NX, canary, RELRO and other mitigations enabled, so normal simple exploitation was not enough.

Honestly most of the time was spent understanding heap behavior and trying not to crash the process.

---

# Main Vulnerabilities

## Bug in Tag Copying

Inside `node_add()` there is a problem with how the tag buffer is handled.

```cpp id="zuvv2s"
tag_len = read_line(cmd_buff, MAX_CMD);

if (strlen(cmd_buff) >= MAX_TAG) {
    PRINT("Tag too long, cutting it off.\n");
    tag_len = MAX_TAG;
    cmd_buff[MAX_TAG - 1] = '\0';
}

memcpy(current_node->tag, cmd_buff, tag_len);
```

The important thing is:

* `MAX_CMD = 25`
* `MAX_TAG = 24`

So there is mismatch between them.

`read_line()` can read more data than the actual tag buffer can safely store. After that, `memcpy()` copies the bytes directly without really validating the final size correctly.

This leads to writing one extra byte after the tag buffer.

At first I thought one byte is probably useless, but actually it becomes enough for corrupting heap metadata.

---

# Heap Corruption

The overflowed byte lands near the next heap chunk metadata.

If the heap layout is prepared carefully, the size field of the next chunk can be corrupted.

Then future allocations start overlapping each other.

This overlap is basically the whole reason the exploit works.

Without overlap there is no control over nearby objects.

Sometimes the heap worked exactly as expected locally, but remotely it behaved slightly different which made debugging painful honestly.

---

# Virtual Function Abuse

The program uses C++ virtual functions.

Something like:

```cpp id="ezs2m5"
class SensorNode {
    virtual void print_desc() { ... }
};
```

Because of this, every object contains a hidden vtable pointer (vptr).

When a virtual function gets called, the binary follows this pointer and jumps to the address stored in the vtable.

If the vptr can be corrupted, execution flow can be redirected somewhere else.

That became the main exploitation target.

---

# Exploitation Steps

## Step 1 — Corrupt the Tag

First I created an authenticated node with a crafted tag payload.

Usually it was:

* many `A` bytes
* then one controlled final byte

The goal was simply to overflow one byte outside the tag buffer and corrupt nearby heap metadata.

Very small corruption, but enough.

---

## Step 2 — Heap Layout

After the corruption, more nodes were allocated.

The corrupted chunk size causes later allocations to overlap with memory belonging to another object.

At this point one node can partially overwrite another node structure or description area.

This is where things started becoming interesting.

A lot of crashes happened here during testing because the heap needed to stay stable enough.

---

## Step 3 — Fake Vtable

After getting overlap, a fake virtual table was written into controlled memory.

Usually the description buffer was the easiest place because its contents are fully attacker controlled.

Inside the fake vtable, the address of `vault_flag()` was placed at the correct offset.

---

## Step 4 — Overwrite vptr

Then the victim object's vptr was overwritten so it pointed to the fake vtable.

Now when the program executes:

```cpp id="zmg2lp"
current_node->print_desc();
```

it no longer calls the real method anymore.

Instead it follows the fake vtable and jumps into our controlled function pointer.

Basically it becomes:

```text id="2d6zmn"
call [fake_vtable + 0x18]
```

which finally reaches:

```text id="cb4g8t"
vault_flag()
```

and prints the flag successfully.

The first time it worked locally was honestly satisfying because before that there were many random crashes.

---

# Another Vulnerability

There was also another bug inside `vault_del_token()`.

The code does this:

```cpp id="iys8cw"
memset(&tokens[id], 0, sizeof(tokens))
```

instead of:

```cpp id="30q0mz"
sizeof(tokens[id])
```

So instead of clearing only one token entry, it clears a huge memory region.

With corrupted `auth_id` values, the memset operation starts wiping nearby memory including parts of `node_list`.

That creates additional corruption possibilities and makes heap reuse easier later.

This bug was actually pretty dangerous.

---

# Stage 2

Stage 2 was harder because calling a single function is much easier than getting full code execution.

The binary protections included:

* PIE
* ASLR
* NX
* Stack Canary
* Full RELRO
* IBT / SHSTK

Because NX is enabled, executing shellcode directly on the heap is not possible.

So a ROP chain or another advanced technique would probably be required.

ASLR and PIE also mean an information leak is needed first before reliable exploitation remotely.

I mostly focused more on the Stage 1 part and understanding the corruption primitives.

---

# Heap Notes

One thing I noticed during the challenge is how sensitive heap exploits are.

Even tiny allocation differences completely change memory layout.

Sometimes adding or removing a single allocation changes everything.

Most overlaps happened between:

* node objects
* description buffers
* heap metadata

So keeping allocations predictable became very important.

---

# Local Debugging

Most testing was done with GDB.

Mainly inspecting:

* vptr addresses
* heap chunks
* node structures
* token arrays
* global node list

After the vptr overwrite was done correctly, calling `print_desc()` redirected execution into `vault_flag()` without crashing.

---

# Files Used During Testing

Some exploit scripts created during testing:

* `exploit_stage1.py`
* `exploit1.py`
* `auth9.py`
* `reinit_token0.py`

Different scripts tested different ideas.

Some focused more on token corruption while others focused on heap overlap and fake vtables.

---

# Final Thoughts

The challenge mainly depended on:

* heap corruption
* overlapping allocations
* fake vtables
* abusing C++ virtual dispatch

The interesting part is that the original bug is only a one-byte overflow, but eventually it can still lead to full control over execution flow.

Overall the hardest thing was not the corruption itself, but making the heap behave consistently enough so the exploit does not randomly die.
