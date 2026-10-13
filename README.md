# jumpbit.com defaults and template repo
This repository is a template for other projects and has default skills and instructions on commonly used frameworks to create new applications.

## Instructions
Main [instructions](.github/copilot.instructions.md) document holds all generic instructions and framework specific instructions.

## Skills
A set of generic [skills](.github/skills/) document standard skills for every project.

## Project features
The project featuers will be stored as markdown in the folder [features](features/).

## Copying the template to a new repository

From the root of this repository, run:

```sh
uv run scripts/sync_template_to_new_repo.py /path/to/new-repo
```

The script uses Rich for its progress, result, and help output and installs its declared dependency with `uv run`. Run it without arguments or with `-h` to see an overview of the copied paths. It also copies `.vscode/settings.json` to apply the template's editor defaults. The destination must be an existing directory. Template files are copied into it; matching files are replaced, while destination-only files are preserved. Use `--no-color` to disable styled terminal output.
