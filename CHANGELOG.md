# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `assets/jumpbit-ui.css`: a very light, Bootstrap-like component and utility layer on the Jump Bit theme (container, 12-column grid, navbar, forms, alerts, badges, tables, list group, spacing/flex/text utilities), using only semantic tokens so light and dark themes work.
- `assets/jumpbit-ui-example.html`: example page showing every component.

### Changed
- Align `assets/` and the styling skill with the Jump Bit design system: Inter is the only typeface for headings, body text and buttons (loaded from `assets/font/`).
- Status text (`.text-*`, Avalonia `Jb*Brush`) uses semantic tokens with readable dark-theme variants; add `--color-on-dark-info` for info text on dark fills.
- The CSS theme also accepts `data-theme="dark|light"` on `<html>`.
- The styling skill's landing example uses the `.landing` layout, `--gradient-brand` and the white logo.
- The template copier's Rich `accent` style is monochrome (`bold`).

### Removed
- Jost/Futura brand font and system-font body stacks (`--font-brand`, `--font-system`, `JbBrandFont`).
- Undefined `--meadow`/`--forest` gradient and `/static/logo.svg` from the styling skill.

### Fixed
- Broken link to the Copilot instructions in the README.
