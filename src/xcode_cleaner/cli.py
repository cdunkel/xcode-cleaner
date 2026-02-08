from __future__ import annotations

import click
from rich.console import Console

from xcode_cleaner import __version__
from xcode_cleaner.cleaner import confirm_deletion, delete_items
from xcode_cleaner.display import (
    display_deletion_summary,
    display_dry_run,
    display_scan_result,
)
from xcode_cleaner.interactive import prompt_selection
from xcode_cleaner.scanner import scan_all

console = Console()


def _run_scan():
    """Run a full scan with a spinner and return the result."""
    with console.status("[bold cyan]Scanning for Xcode files...[/bold cyan]"):
        result = scan_all()
    return result


@click.group()
@click.version_option(version=__version__)
def main():
    """Reclaim disk space from Xcode build artifacts, caches, and simulators."""


@main.command()
def scan():
    """Scan and display Xcode disk usage report."""
    result = _run_scan()
    display_scan_result(result)


@main.command()
@click.option("--dry-run", is_flag=True, help="Show what would be deleted without deleting.")
def clean(dry_run: bool):
    """Interactively select and delete Xcode files to free disk space."""
    result = _run_scan()

    if result.grand_total == 0:
        console.print("[green]Nothing to clean — all categories are empty.[/green]")
        return

    display_scan_result(result)

    selected = prompt_selection(result)
    if not selected:
        console.print("No items selected.")
        return

    if dry_run:
        display_dry_run(selected)
        return

    if not confirm_deletion(selected):
        console.print("Cancelled.")
        return

    results = delete_items(selected)
    display_deletion_summary(results)
