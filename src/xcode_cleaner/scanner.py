from __future__ import annotations

from pathlib import Path

from xcode_cleaner.constants import CATEGORY_PATHS, Category
from xcode_cleaner.models import ScanCategory, ScanItem, ScanResult
from xcode_cleaner.simulators import list_simulators
from xcode_cleaner.sizes import dir_size


def _scan_flat(category: Category, base: Path) -> list[ScanItem]:
    """Scan a directory where each subdirectory is one item."""
    if not base.is_dir():
        return []
    items: list[ScanItem] = []
    try:
        for entry in sorted(base.iterdir()):
            if entry.is_dir() and not entry.is_symlink():
                size = dir_size(entry)
                items.append(
                    ScanItem(
                        name=entry.name,
                        size_bytes=size,
                        category=category,
                        path=entry,
                    )
                )
    except PermissionError:
        pass
    return items


def _scan_archives(base: Path) -> list[ScanItem]:
    """Scan Archives — date folders containing .xcarchive bundles."""
    if not base.is_dir():
        return []
    items: list[ScanItem] = []
    try:
        for date_folder in sorted(base.iterdir()):
            if not date_folder.is_dir() or date_folder.is_symlink():
                continue
            for archive in sorted(date_folder.iterdir()):
                if archive.is_dir() and not archive.is_symlink() and archive.suffix == ".xcarchive":
                    size = dir_size(archive)
                    items.append(
                        ScanItem(
                            name=archive.name,
                            size_bytes=size,
                            category=Category.ARCHIVES,
                            path=archive,
                            metadata={"date_folder": date_folder.name},
                        )
                    )
    except PermissionError:
        pass
    return items


def scan_category(category: Category) -> ScanCategory:
    """Scan a single category and return results."""
    if category == Category.SIMULATORS:
        items, found = list_simulators()
    elif category == Category.ARCHIVES:
        base = CATEGORY_PATHS[Category.ARCHIVES]
        found = base.is_dir()
        items = _scan_archives(base)
    else:
        base = CATEGORY_PATHS[category]
        found = base.is_dir()
        items = _scan_flat(category, base)

    # Sort by size descending
    items.sort(key=lambda x: x.size_bytes, reverse=True)
    return ScanCategory(category=category, items=items, found=found)


def scan_all() -> ScanResult:
    """Scan all categories and return a full result."""
    categories = [scan_category(cat) for cat in Category]
    return ScanResult(categories=categories)
