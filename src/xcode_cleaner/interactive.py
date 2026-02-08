from __future__ import annotations

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from xcode_cleaner.models import ScanItem, ScanResult
from xcode_cleaner.sizes import format_size


def prompt_selection(result: ScanResult) -> list[ScanItem]:
    """Show an interactive checkbox prompt grouped by category. Returns selected items."""
    choices: list[Choice | Separator] = []
    items_by_index: dict[int, ScanItem] = {}
    index = 0

    for scan_cat in result.categories:
        if not scan_cat.items:
            continue

        choices.append(
            Separator(
                f"── {scan_cat.category.value} ({scan_cat.item_count} items, {format_size(scan_cat.total_size)}) ──"
            )
        )

        for item in scan_cat.items:
            items_by_index[index] = item
            choices.append(
                Choice(
                    value=index,
                    name=f"{item.name}  ({format_size(item.size_bytes)})",
                    enabled=False,
                )
            )
            index += 1

    if not choices:
        return []

    selected = inquirer.checkbox(
        message="Select items to delete (Space to toggle, Enter to confirm):",
        choices=choices,
        cycle=True,
        instruction="(↑/↓ navigate, Space toggle, Enter confirm)",
    ).execute()

    if not selected:
        return []

    return [items_by_index[i] for i in selected]
