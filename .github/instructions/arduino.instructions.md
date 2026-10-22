---
description: "Use when developing Arduino sketches or PlatformIO projects, including board selection, libraries, GPIO, and peripheral code."
applyTo: "**/*.ino,**/*.pde,**/platformio.ini"
---

# Arduino Development Guidelines

https://github.com/arduino/arduino-cli

- Follow the board's documented voltage, pin capabilities, and peripheral constraints; do not assume pin mappings are portable across boards.
- Keep board and library dependencies explicit and use stable, compatible versions where the project supports pinning.
- Avoid long `delay()` calls in application logic; use `millis()`-based timing or the project's established scheduling pattern so other work can proceed.
- Check return values from APIs that can fail, including peripheral initialization and reads; report failures rather than continuing with invalid data.
- On memory-constrained boards, prefer bounded buffers and predictable allocation; avoid repeated dynamic allocation in long-running paths.
- Keep hardware-specific behavior behind small functions or interfaces when the same sketch supports multiple boards.
- Verify behavior on the target board, including startup, reset, and peripheral failure cases.
