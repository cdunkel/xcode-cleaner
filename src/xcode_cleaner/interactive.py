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

        # Compute column widths for alignment within this category
        name_width = 0
        state_width = 0
        size_width = 0
        for item in scan_cat.items:
            name_width = max(name_width, len(item.name))
            state = item.metadata.get("state", "")
            if state:
                state_width = max(state_width, len(f"[{state}]"))
            size_width = max(size_width, len(format_size(item.size_bytes)))

        for item in scan_cat.items:
            items_by_index[index] = item
            state = item.metadata.get("state", "")
            state_str = f"[{state}]" if state else ""
            size_str = format_size(item.size_bytes)

            name_col = item.name.ljust(name_width)
            state_col = state_str.ljust(state_width) if state_width else ""
            size_col = size_str.rjust(size_width)

            parts = [name_col]
            if state_width:
                parts.append(state_col)
            parts.append(size_col)

            choices.append(
                Choice(
                    value=index,
                    name="  ".join(parts),
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
