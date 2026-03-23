# Lesson 17 — CMake Basics

## Overview

CMake is the standard build system generator for C++ projects. It reads a `CMakeLists.txt` file and generates platform-native build files (Makefiles on Linux/macOS, Visual Studio projects on Windows, Ninja files, etc.). You write one `CMakeLists.txt` — CMake handles the rest.

---

## Why CMake

| Without CMake | With CMake |
|---------------|-----------|
| Different compiler commands per OS | One `CMakeLists.txt` works everywhere |
| Manual dependency tracking | CMake tracks what to rebuild |
| Managing include paths by hand | `target_include_directories` handles it |
| Fetching libraries manually | `FetchContent` downloads and links them |

---

## Minimal `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.20)    # minimum CMake version
project(MyApp VERSION 1.0)              # project name (and optional version)

set(CMAKE_CXX_STANDARD 20)             # require C++20
set(CMAKE_CXX_STANDARD_REQUIRED ON)    # error if compiler doesn't support it
set(CMAKE_CXX_EXTENSIONS OFF)          # use -std=c++20, not -std=gnu++20

add_executable(MyApp main.cpp)          # build 'MyApp' from main.cpp
```

---

## Build Commands

```bash
# Step 1: configure — reads CMakeLists.txt, generates build files in ./build
cmake -B build

# Step 2: build — compiles and links
cmake --build build

# Run the output
./build/MyApp
```

The `-B build` flag puts all generated files in a `build/` directory, keeping the source tree clean. Never commit the `build/` directory.

```bash
# Add to .gitignore
build/
```

---

## Multiple Source Files

```cmake
add_executable(MyApp
    main.cpp
    src/utils.cpp
    src/database.cpp
)
```

Or use a glob (less preferred — CMake won't auto-detect new files):

```cmake
file(GLOB_RECURSE SOURCES "src/*.cpp")
add_executable(MyApp ${SOURCES})
```

---

## Include Directories

```cmake
target_include_directories(MyApp PRIVATE include/)
```

- `PRIVATE` — only `MyApp` itself needs these headers
- `PUBLIC` — `MyApp` and anything that links to it needs them
- `INTERFACE` — only things that link to `MyApp` need them (not `MyApp` itself)

---

## Libraries

### Creating a Library

```cmake
add_library(MathLib STATIC      # or SHARED for a .so/.dll
    src/math.cpp
)

target_include_directories(MathLib PUBLIC include/)

add_executable(MyApp main.cpp)
target_link_libraries(MyApp PRIVATE MathLib)
```

### Linking System Libraries

```cmake
# Link threads library (portable across platforms)
find_package(Threads REQUIRED)
target_link_libraries(MyApp PRIVATE Threads::Threads)
```

---

## FetchContent — Downloading Dependencies

`FetchContent` downloads and integrates a dependency at configure time:

```cmake
include(FetchContent)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
FetchContent_MakeAvailable(googletest)

add_executable(MyTests test_main.cpp)
target_link_libraries(MyTests PRIVATE GTest::gtest_main)
```

---

## Compiler Warnings and Settings

```cmake
# Add warnings — good practice for catching bugs
target_compile_options(MyApp PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
)
```

---

## Build Types

```bash
# Debug build — includes debug info, no optimization
cmake -B build -DCMAKE_BUILD_TYPE=Debug

# Release build — optimized, no debug info
cmake -B build -DCMAKE_BUILD_TYPE=Release

# RelWithDebInfo — optimized + debug info (useful for profiling)
cmake -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

---

## Typical Project Structure

```
MyProject/
├── CMakeLists.txt
├── src/
│   ├── main.cpp
│   └── utils.cpp
├── include/
│   └── utils.h
├── tests/
│   ├── CMakeLists.txt
│   └── test_utils.cpp
└── build/          ← generated; in .gitignore
```

For a project with tests, the root `CMakeLists.txt` can include subdirectories:

```cmake
add_subdirectory(src)
add_subdirectory(tests)
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Editing files in `build/` | Rebuild is generated — edit `CMakeLists.txt` instead |
| `cmake .` without `-B` | Pollutes source directory with build files — always use `-B build` |
| Not setting `CMAKE_CXX_STANDARD` | Defaults to C++98 — set it explicitly |
| Using `file(GLOB ...)` for sources | CMake won't re-configure when files are added — list files explicitly or re-run cmake |
| Committing the `build/` directory | Add `build/` to `.gitignore` |

---

## Quick Reference Card

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Executable
add_executable(MyApp main.cpp src/foo.cpp)
target_include_directories(MyApp PRIVATE include/)

# Library
add_library(MyLib STATIC src/mylib.cpp)
target_include_directories(MyLib PUBLIC include/)
target_link_libraries(MyApp PRIVATE MyLib)

# Fetch a dependency
include(FetchContent)
FetchContent_Declare(dep GIT_REPOSITORY <url> GIT_TAG <tag>)
FetchContent_MakeAvailable(dep)
target_link_libraries(MyApp PRIVATE dep::dep)

# Compiler warnings
target_compile_options(MyApp PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>
)
```

```bash
# Build commands
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/MyApp
```
