from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from xcode_cleaner.constants import Category
from xcode_cleaner.models import DeletionResult, ScanResult
from xcode_cleaner.sizes import format_size

console = Console()


def display_scan_result(result: ScanResult) -> None:
    """Display the scan result as Rich tables grouped by category."""
    for scan_cat in result.categories:
        if not scan_cat.items:
            console.print(f"[bold cyan]{scan_cat.category.value}[/bold cyan]")
            if not scan_cat.found:
                if scan_cat.category in (Category.SIMULATORS, Category.SIMULATOR_RUNTIMES):
                    console.print("  [dim]Could not list (xcrun unavailable)[/dim]")
                else:
                    console.print("  [dim]Directory not found — skipped[/dim]")
            else:
                console.print("  [dim]Empty — nothing to clean[/dim]")
            console.print()
            continue

        table = Table(
            title=f"{scan_cat.category.value}",
            title_style="bold cyan",
            show_lines=False,
        )
        table.add_column("Name", style="white", no_wrap=False, ratio=3)
        table.add_column("Size", style="green", justify="right", ratio=1)

        for item in scan_cat.items:
            table.add_row(item.name, format_size(item.size_bytes))

        table.add_section()
        table.add_row(
            f"[bold]{scan_cat.item_count} items[/bold]",
            f"[bold]{format_size(scan_cat.total_size)}[/bold]",
        )

        console.print(table)
        console.print()

    console.print(
        Panel(
            f"[bold]Total reclaimable space: {format_size(result.grand_total)}[/bold]",
            style="green",
        )
    )


def display_deletion_summary(results: list[DeletionResult]) -> None:
    """Display summary of deletion results."""
    succeeded = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    freed = sum(r.item.size_bytes for r in succeeded)

    console.print()
    if succeeded:
        console.print(
            f"[green]Deleted {len(succeeded)} item(s), freed {format_size(freed)}[/green]"
        )
    if failed:
        console.print(f"[red]Failed to delete {len(failed)} item(s):[/red]")
        for r in failed:
            console.print(f"  [red]• {r.item.name}: {r.error}[/red]")


def display_dry_run(items: list) -> None:
    """Display what would be deleted in dry-run mode."""
    from xcode_cleaner.models import ScanItem

    total = sum(item.size_bytes for item in items)
    console.print(
        Panel("[bold yellow]Dry run — nothing will be deleted[/bold yellow]")
    )
    for item in items:
        console.print(f"  Would delete: {item.name} ({format_size(item.size_bytes)})")
    console.print(
        f"\n[bold]Would free {format_size(total)} across {len(items)} item(s)[/bold]"
    )
