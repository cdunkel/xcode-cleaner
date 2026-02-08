from __future__ import annotations

import shutil

from rich.progress import Progress

from xcode_cleaner.display import console
from xcode_cleaner.models import DeletionResult, ScanItem
from xcode_cleaner.simulators import delete_simulator
from xcode_cleaner.sizes import format_size


def confirm_deletion(items: list[ScanItem]) -> bool:
    """Ask the user to confirm deletion."""
    total = sum(item.size_bytes for item in items)
    console.print(
        f"\n[bold yellow]Delete {len(items)} item(s) ({format_size(total)})? "
        f"This cannot be undone.[/bold yellow]"
    )
    answer = console.input("[bold]Proceed? (y/N): [/bold]").strip().lower()
    return answer in ("y", "yes")


def delete_items(items: list[ScanItem]) -> list[DeletionResult]:
    """Delete the selected items, returning results for each."""
    results: list[DeletionResult] = []

    with Progress(console=console) as progress:
        task = progress.add_task("Deleting...", total=len(items))
        for item in items:
            try:
                if item.item_id is not None:
                    # Simulator — use simctl
                    delete_simulator(item.item_id)
                elif item.path is not None:
                    shutil.rmtree(item.path)
                else:
                    raise ValueError("Item has no path or item_id")
                results.append(DeletionResult(item=item, success=True))
            except Exception as exc:
                results.append(
                    DeletionResult(item=item, success=False, error=str(exc))
                )
            progress.advance(task)

    return results
