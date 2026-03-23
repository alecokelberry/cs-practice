# 04 — Debugging & Sanitizers

Debugging is the process of finding and fixing the gap between what your code *does* and what you *expect* it to do. The goal is to shrink the unknown — narrow down where the bug lives until it's obvious.

---

## Mental Model

A bug is a wrong assumption somewhere in your code. Debugging is the process of finding which assumption is wrong.

```
Expected:  program outputs 10
Actual:    program outputs 8

Question: where does the value first become wrong?
→ Add checkpoints (prints or breakpoints) to find the split point
→ Once you find the first place it's wrong, you know the bug is before or at that point
```

The key insight: **don't fix what you haven't found yet.** Guessing and changing random things wastes time. Localize first, fix second.

---

## Strategy: Scientific Debugging

1. **Observe** — what exactly is wrong? (exact output, error message, wrong value)
2. **Hypothesize** — what could cause this? (pick the most likely candidate)
3. **Test** — add a print or breakpoint to check your hypothesis
4. **Conclude** — was your hypothesis right? If yes, fix it. If no, update the hypothesis.
5. **Repeat** until localized

This is faster than staring at code and thinking.

---

## Print / Log Debugging

The simplest and most universally applicable technique. Works in any language, any environment.

### In Python

```python
# Basic
print(f"DEBUG: value = {value}")
print(f"DEBUG: type = {type(value)}, value = {value!r}")  # !r shows repr

# Print the whole object
print(f"DEBUG: user = {vars(user)}")

# Track control flow
def process(items):
    print(f"DEBUG: process called with {len(items)} items")
    for i, item in enumerate(items):
        print(f"DEBUG:   [{i}] {item!r}")
        # ... rest of function

# Use logging instead of print in real code
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("value = %s", value)
logging.info("Processing %d items", len(items))
```

### In C++

```cpp
#include <iostream>

// Simple trace macro (disabled in release builds)
#define DEBUG_PRINT(x) std::cerr << "DEBUG: " << #x << " = " << (x) << "\n"

int main() {
    int x = 5;
    DEBUG_PRINT(x);         // prints: DEBUG: x = 5
    DEBUG_PRINT(x * 2);     // prints: DEBUG: x * 2 = 10
}
```

### Best practices

- Use `stderr` (`std::cerr`, `sys.stderr`) for debug output so it doesn't mix with actual program output
- Remove debug prints before committing — or use a proper logging framework with levels
- Be specific: `"value = 42"` is more useful than `"here"`
- Print at **entry and exit** of functions you're suspicious about

---

## Using a Debugger (GDB)

GDB (GNU Debugger) is the standard debugger for C and C++ on Linux/macOS. It lets you pause execution, inspect variables, and step through code line by line.

### Basic session

```bash
# Compile with debug info (required — without -g, GDB has no source info)
g++ -g -std=c++20 main.cpp -o main

# Start GDB
gdb ./main
```

### Core commands

```
(gdb) run                    # start the program
(gdb) run arg1 arg2          # start with arguments

(gdb) break main             # set breakpoint at function 'main'
(gdb) break main.cpp:42      # set breakpoint at line 42
(gdb) info breakpoints       # list all breakpoints
(gdb) delete 1               # delete breakpoint 1

(gdb) next        (n)        # run next line (step over function calls)
(gdb) step        (s)        # run next line (step INTO function calls)
(gdb) continue    (c)        # run until next breakpoint
(gdb) finish                 # run until current function returns

(gdb) print x                # print value of variable x
(gdb) print *ptr             # dereference and print a pointer
(gdb) print arr[0]           # print array element
(gdb) info locals            # print all local variables
(gdb) info args              # print function arguments

(gdb) backtrace   (bt)       # show call stack
(gdb) frame 2                # switch to stack frame 2

(gdb) quit        (q)        # exit GDB
```

### Investigating a crash

```bash
# If your program crashes and creates a core dump:
g++ -g main.cpp -o main
./main             # crashes
gdb ./main core    # open the core dump

(gdb) backtrace    # see the call stack at the moment of crash
(gdb) frame 0      # go to the crashing frame
(gdb) info locals  # see what variables look like there
```

### Tip: GDB TUI mode

```bash
gdb -tui ./main    # split-screen with source code + gdb commands
```

---

## VS Code Debugger

VS Code has a built-in graphical debugger. It's much easier to use than GDB for everyday work.

### Setup for C++ (launch.json)

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug C++",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/main",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "build"
        }
    ]
}
```

### Setup for Python (launch.json)

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Python",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```

### Key VS Code debugger features

- **Breakpoints** — click in the gutter (left of line numbers)
- **Conditional breakpoints** — right-click → "Add Conditional Breakpoint" (e.g., `i == 5`)
- **Watch expressions** — add variables or expressions to watch panel
- **Call stack** — see the full chain of function calls
- **Step over (F10)** — next line, don't enter functions
- **Step into (F11)** — next line, enter functions
- **Step out (Shift+F11)** — finish current function, return to caller
- **Continue (F5)** — run until next breakpoint

---

## Sanitizers (C++)

Sanitizers are compiler tools that instrument your code at compile time to detect bugs at runtime. They catch things that are otherwise silent — undefined behavior, memory errors, data races.

### AddressSanitizer (ASan)

Detects: buffer overflow, use-after-free, heap corruption, stack overflow.

```bash
g++ -fsanitize=address -g -std=c++20 main.cpp -o main && ./main
```

Example — reading out of bounds:
```cpp
int arr[5] = {1, 2, 3, 4, 5};
std::cout << arr[10];  // undefined behavior — silent without ASan
```

With ASan:
```
==12345==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x...
READ of size 4 at 0x... thread T0
    #0 main (main.cpp:4)
```

### UndefinedBehaviorSanitizer (UBSan)

Detects: signed integer overflow, null pointer dereference, invalid casts, shift by negative.

```bash
g++ -fsanitize=undefined -g -std=c++20 main.cpp -o main && ./main
```

Example — signed overflow:
```cpp
int x = INT_MAX;
int y = x + 1;  // undefined behavior — silent without UBSan
```

With UBSan:
```
main.cpp:3: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

### ThreadSanitizer (TSan)

Detects: data races in multithreaded code.

```bash
g++ -fsanitize=thread -g -std=c++20 main.cpp -o main && ./main
```

### Using multiple sanitizers

```bash
# ASan + UBSan together (common combination)
g++ -fsanitize=address,undefined -g -std=c++20 main.cpp -o main && ./main
```

**Note:** Don't use ASan and TSan together — they conflict.

### Sanitizers in Python

Python has no compile step, but you can use:

```bash
# Valgrind (for C extension memory bugs)
valgrind --leak-check=full python3 my_script.py

# Python's built-in tracemalloc (memory allocation tracking)
python3 -m tracemalloc my_script.py
```

---

## Valgrind

Valgrind is a memory error detector for C/C++. Slower than ASan but catches slightly different issues.

```bash
# Install (Linux)
sudo apt install valgrind

# Check for memory leaks and errors
valgrind --leak-check=full --error-exitcode=1 ./main
```

Common Valgrind errors:
- `Invalid read/write` — out-of-bounds access
- `Use of uninitialised value` — reading uninitialized memory
- `definitely lost` — memory leaked (allocated, never freed)
- `Invalid free` — freeing a pointer twice or a non-heap pointer

---

## Reading Error Messages

Error messages tell you the "what" and "where" — reading them carefully saves a lot of time.

### Segmentation fault (C++)

```
Segmentation fault (core dumped)
```

This means your program tried to access memory it doesn't own. Most common causes:
- Null pointer dereference (`*ptr` when `ptr == nullptr`)
- Out-of-bounds array access
- Stack overflow (infinite recursion)
- Use-after-free (accessing memory after `delete`)

Debug with: `-fsanitize=address` or GDB.

### Stack trace (Python)

```
Traceback (most recent call last):
  File "main.py", line 12, in <module>
    result = process(data)
  File "main.py", line 7, in process
    return data[index]
IndexError: list index out of range
```

Read bottom-up: the error is `IndexError` on line 7 inside `process()`, which was called from line 12. The bug is on line 7 — `index` is out of range.

### Compiler error vs linker error (C++)

- **Compiler error** — syntax or type error in your source code. Fix in your `.cpp` file.
- **Linker error** — `undefined reference to 'foo'` — you declared something but didn't define it, or forgot to link a library.

```bash
# Linker error example
g++ main.cpp -o main
# /usr/bin/ld: undefined reference to 'some_function'
# → you forgot to include the .cpp that defines 'some_function'
g++ main.cpp other.cpp -o main  # fix: compile all files together
```

---

## Debugging Checklist

When something is wrong, go through this before assuming it's complicated:

1. **Read the error message carefully** — the exact message, file, and line number
2. **Reproduce it reliably** — can you make it happen every time?
3. **Find the smallest reproducing case** — remove everything not needed to trigger the bug
4. **Check your assumptions** — print the values you think you know
5. **Search for the last known-good state** — where was the value correct?
6. **Use a sanitizer or debugger** — don't just stare at code

---

## Common Pitfalls

**Changing too many things at once**
When debugging, change one thing at a time. If you change three things and the bug goes away, you don't know which one fixed it — and you might have introduced a new bug with one of the others.

**Trusting the compiler to catch everything**
The compiler catches type errors and syntax errors. It doesn't catch logic errors, out-of-bounds access, or use-after-free. That's what sanitizers and tests are for.

**Not using `-g` when compiling for GDB**
Without `-g`, GDB shows machine code addresses, not source lines. Always compile with `-g` when debugging.

**Print statements that lie**
`std::cout` has buffering — it might not flush immediately. Use `std::cerr` for debug output (unbuffered), or add `<< std::flush` or `<< std::endl` to force a flush.

```cpp
// May not print before crash
std::cout << "DEBUG: before crash\n";

// Guaranteed to appear before crash
std::cerr << "DEBUG: before crash\n";
```

---

## Quick Reference

```
Strategy
  1. Reproduce reliably
  2. Find the smallest reproducing case
  3. Locate the first point where the value is wrong
  4. Fix, test, verify

Print debugging
  std::cerr << "DEBUG: x = " << x << "\n";   // C++ (unbuffered)
  print(f"DEBUG: {x = }")                     # Python 3.8+ (f-string with =)
  logging.debug("x = %s", x)                 # Python with logging module

GDB essentials
  g++ -g file.cpp -o prog    # compile with debug info
  gdb ./prog                 # start debugger
  break main                 # breakpoint at function
  break file.cpp:42          # breakpoint at line
  run                        # start program
  next / step / continue     # n, s, c
  print x                    # inspect variable
  backtrace                  # see call stack
  quit                       # exit

Sanitizers (C++)
  -fsanitize=address          # ASan: buffer overflow, use-after-free
  -fsanitize=undefined        # UBSan: signed overflow, null deref
  -fsanitize=address,undefined  # both together (common combo)
  -fsanitize=thread           # TSan: data races (don't mix with ASan)

Always compile with -g when using sanitizers or GDB

VS Code debugger
  F5          → start / continue
  F10         → step over
  F11         → step into
  Shift+F11   → step out
  Click gutter → toggle breakpoint
```
