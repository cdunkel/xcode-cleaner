from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from xcode_cleaner.constants import Category


@dataclass
class ScanItem:
    name: str
    size_bytes: int
    category: Category
    path: Path | None = None
    item_id: str | None = None  # UDID for simulators
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class ScanCategory:
    category: Category
    items: list[ScanItem] = field(default_factory=list)
    found: bool = True  # Whether the source directory/data was found

    @property
    def total_size(self) -> int:
        return sum(item.size_bytes for item in self.items)

    @property
    def item_count(self) -> int:
        return len(self.items)


@dataclass
class ScanResult:
    categories: list[ScanCategory] = field(default_factory=list)

    @property
    def grand_total(self) -> int:
        return sum(cat.total_size for cat in self.categories)


@dataclass
class DeletionResult:
    item: ScanItem
    success: bool
    error: str | None = None
