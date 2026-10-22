---
applyTo: "**/*.cpp,**/*.cc,**/*.cxx,**/*.hpp,**/*.hh,**/*.hxx"
description: "Modern C++ language, memory safety, tooling and testing rules"
---

# C++ Guidelines
https://isocpp.github.io/CppCoreGuidelines/

## Purpose
Rules for writing and reviewing C++ code for applications, libraries and embedded systems. Target: **C++23**; use C++26 features only when every compiler the project builds with supports them. Platform rules come first: follow [arduino.instructions.md](./arduino.instructions.md) for Arduino sketches and [nrf.instructions.md](./nrf.instructions.md) for nRF Connect SDK / Zephyr projects. For C code and shared C headers follow [c.instructions.md](./c.instructions.md).

Always check the standard set in the build system (`CMAKE_CXX_STANDARD`, `-std=`) first and only use features available there; never raise it silently. Follow the C++ Core Guidelines where this file says nothing.

## Tooling
- Build with CMake (presets in `CMakePresets.json`) and manage third-party libraries with vcpkg or Conan in manifest mode with committed versions.
- Compile with warnings as errors: `-Wall -Wextra -Wpedantic -Wshadow -Wconversion -Werror` (GCC/Clang) or `/W4 /WX` (MSVC). Don't silence warnings without a comment explaining why.
- Format with `clang-format` using the committed `.clang-format`; lint with `clang-tidy` (`cppcoreguidelines-*`, `modernize-*`, `bugprone-*`). Code must pass both with zero warnings.
- Run tests with AddressSanitizer and UndefinedBehaviorSanitizer in CI; ThreadSanitizer for concurrent code.

## Style and naming
- Follow the project's existing naming; default: `PascalCase` for types, `snake_case` or `camelCase` for functions and variables (one style project-wide), `kPascalCase` or `UPPER_SNAKE_CASE` for constants, trailing `_` for private members.
- Put code in a project namespace; never `using namespace` in headers.
- Headers use `#pragma once`, include what they use and keep implementation details out of the public API.

## Language
- RAII for every resource; no naked `new`/`delete`. Use `std::unique_ptr` by default, `std::shared_ptr` only for real shared ownership, and `std::make_unique`/`std::make_shared`.
- Prefer value semantics, `const` and `constexpr`/`consteval`; follow the rule of zero, otherwise the rule of five.
- Use `std::span`, `std::string_view` and ranges instead of pointer-and-length pairs; `std::array` and `std::vector` instead of C arrays.
- Use `std::expected` (C++23) or the project's error type for expected failures; exceptions only for truly exceptional errors and only where the platform allows them. Mark functions that don't throw `noexcept`.
- Use `[[nodiscard]]` on functions whose result must be used, `enum class` instead of plain `enum`, and `std::format`/`std::print` instead of `printf` or iostream formatting.
- Use concepts to constrain templates; avoid macros except for include guards and platform switches.
- Avoid undefined behavior: no out-of-bounds access, dangling references or views, signed overflow, or data races.

## Concurrency
- Use `std::jthread` with `std::stop_token`, and `std::mutex` with `std::scoped_lock`; protect shared mutable state or avoid it.
- Prefer message passing and immutable data over shared state; use `std::atomic` only for simple flags and counters.

## Embedded
- Build with `-fno-exceptions -fno-rtti` only where the platform requires it, and then use `std::expected`-style error handling consistently.
- Avoid heap allocation after startup; use fixed-capacity containers (`std::array`, `std::inplace_vector` in C++26, or the project's static containers) and `std::pmr` with a static buffer where allocation is needed.
- Keep interrupt handlers minimal and defer work to a thread, task or main loop.

## Security
- Validate all external input at the boundary; check sizes before copying or casting.
- Never store secrets in source code; read them from the environment or secure storage.

## Documentation
- Doc comments in Doxygen format (`///` or `/** ... */`) on public types and functions; comments explain *why*.

## Testing
- Use GoogleTest or Catch2 (whichever the project uses) via CTest; tests in `tests/` mirroring the source structure.
- Every bug fix includes a test that fails without the fix; mock hardware and external services behind interfaces.
