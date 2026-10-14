# jumpbit.com defaults and template repo
This repository is a template for other projects and has default skills and instructions on commonly used frameworks to create new applications.

## Instructions
Main [instructions](.github/copilot-instructions.md) document holds all generic instructions and framework specific instructions.

## Skills
A set of generic [skills](.github/skills/) document standard skills for every project.

## Design system
The jumpbit.com corporate identity follows the **Jump Bit** design system (https://claude.ai/artifact/FchxsJbujLEuHSzFKx4VK8). [assets/](assets/) implements it:

- [jumpbit-tokens.json](assets/jumpbit-tokens.json) — colour, typography and radius tokens.
- [jumpbit-theme.css](assets/jumpbit-theme.css) — CSS custom properties and base, button, card, status and landing styles; light and dark themes.
- [jumpbit-theme.axaml](assets/jumpbit-theme.axaml) and [jumpbit-styles.axaml](assets/jumpbit-styles.axaml) — the same for Avalonia.
- Inter variable fonts in [assets/font/](assets/font/), the only typeface; logos, favicons, app icons and `site.webmanifest`.

The [styling skill](.github/skills/styling/SKILL.md) describes how to apply it.

## Project features
The project features will be stored as markdown in the folder [features](features/).

## Copying the template to a new repository

From the root of this repository, run:

```sh
uv run scripts/sync_template_to_new_repo.py /path/to/new-repo
```

The script uses Rich for its progress, result, and help output and installs its declared dependency with `uv run`. Run it without arguments or with `-h` to see an overview of the copied paths. It also copies `.vscode/settings.json` to apply the template's editor defaults. The destination must be an existing directory. Template files are copied into it; matching files are replaced, while destination-only files are preserved. Use `--no-color` to disable styled terminal output.
