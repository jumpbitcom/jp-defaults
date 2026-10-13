"""Copy this repository's template files into an existing repository directory."""

# /// script
# requires-python = ">=3.12"
# dependencies = ["rich>=15,<16"]
# ///

import argparse
import shutil
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table
from rich.theme import Theme

TEMPLATE_PATHS = (
    "assets",
    ".github",
    ".claude",
    ".vscode/settings.json",
    "CLAUDE.md",
)
THEME = Theme(
    {
        "accent": "bold cyan",
        "success": "bold green",
        "error": "bold red",
    }
)


def show_description(console: Console) -> None:
    """Show a quick, styled overview of the template copy operation."""
    console.print(
        Panel(
            "Copy the shared project defaults into a new repository.",
            title="[accent]Repository Template Copier[/accent]",
            subtitle="Merge defaults without removing destination-only files",
            border_style="accent",
            expand=False,
        )
    )

    table = Table(title="Included template paths")
    table.add_column("Path", style="accent")
    table.add_column("Contents")
    table.add_row("assets/", "Shared project assets")
    table.add_row(".github/", "GitHub instructions, agents, prompts, and skills")
    table.add_row(".claude/", "Claude Code instructions and skills")
    table.add_row(".vscode/settings.json", "VS Code editor defaults")
    table.add_row("CLAUDE.md", "Claude Code project guidance")
    console.print(table)
    console.print(
        "\n[accent]Usage[/accent]  "
        "uv run scripts/sync_template_to_new_repo.py [bold]<repository-path>[/bold]"
    )
    console.print(
        "[dim]Run without arguments or with -h/--help to show this overview. "
        "Use --no-color for plain output.[/dim]"
    )


def get_copy_plan(destination: Path, template_root: Path) -> list[tuple[Path, Path]]:
    """Validate paths and return the template files and directories to copy."""
    if not destination.is_dir():
        raise NotADirectoryError(
            f"Destination must be an existing directory: {destination}"
        )

    if destination == template_root or destination in template_root.parents:
        raise ValueError(
            "Destination cannot be the template repository or one of its parents."
        )
    if template_root in destination.parents:
        raise ValueError("Destination cannot be inside the template repository.")

    sources = [(template_root / name, destination / name) for name in TEMPLATE_PATHS]
    missing = [source for source, _ in sources if not source.exists()]
    if missing:
        raise FileNotFoundError(
            f"Template paths do not exist: {', '.join(map(str, missing))}"
        )

    return sources


def copy_path(source: Path, target: Path) -> None:
    """Copy a directory tree or file to its corresponding destination."""
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "repository",
        type=Path,
        nargs="?",
        help="path to the destination repository",
    )
    parser.add_argument("-h", "--help", action="store_true", help="show this overview")
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable color",
    )
    args = parser.parse_args()

    console = Console(theme=THEME, no_color=args.no_color)
    if args.help or args.repository is None:
        show_description(console)
        return 0

    template_root = Path(__file__).resolve().parent.parent
    destination = args.repository.expanduser().resolve()
    err_console = Console(stderr=True, theme=THEME, no_color=args.no_color)

    try:
        copy_plan = get_copy_plan(destination, template_root)
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=True,
        ) as progress:
            task_id = progress.add_task(
                "Copying template files...", total=len(copy_plan)
            )
            for source, target in copy_plan:
                copy_path(source, target)
                progress.advance(task_id)
    except (OSError, ValueError) as error:
        err_console.print(
            f"[error]Could not copy template files:[/error] {escape(str(error))}"
        )
        return 1

    table = Table(title="Template files copied")
    table.add_column("Path")
    for path in TEMPLATE_PATHS:
        table.add_row(path)
    console.print(table)
    console.print(f"[success]Destination:[/success] {escape(str(destination))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
