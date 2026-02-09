from __future__ import annotations

import shutil

from rich.progress import Progress

from xcode_cleaner.constants import CATEGORY_PATHS, DEVICE_SUPPORT_PATHS, Category
from xcode_cleaner.display import console
from xcode_cleaner.models import DeletionResult, ScanItem
from xcode_cleaner.simulators import delete_runtime, delete_simulator
from xcode_cleaner.sizes import format_size

# Resolved allowed base directories for path validation
_ALLOWED_BASES = tuple(
    p.resolve() for p in (*CATEGORY_PATHS.values(), *DEVICE_SUPPORT_PATHS)
)


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
                    if item.category == Category.SIMULATOR_RUNTIMES:
                        delete_runtime(item.item_id)
                    else:
                        delete_simulator(item.item_id)
                elif item.path is not None:
                    if item.path.is_symlink():
                        item.path.unlink()
                    else:
                        resolved = item.path.resolve()
                        if not any(
                            resolved == base or str(resolved).startswith(str(base) + "/")
                            for base in _ALLOWED_BASES
                        ):
                            raise ValueError(
                                f"Refusing to delete {resolved}: outside expected Xcode directories"
                            )
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
