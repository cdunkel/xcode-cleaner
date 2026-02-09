from __future__ import annotations

from enum import Enum
from pathlib import Path


class Category(Enum):
    DERIVED_DATA = "Derived Data"
    ARCHIVES = "Archives"
    SIMULATORS = "Simulators"
    SIMULATOR_RUNTIMES = "Simulator Runtimes"
    CACHES = "Xcode Caches"


XCODE_BASE = Path.home() / "Library" / "Developer" / "Xcode"

CATEGORY_PATHS: dict[Category, Path] = {
    Category.DERIVED_DATA: XCODE_BASE / "DerivedData",
    Category.ARCHIVES: XCODE_BASE / "Archives",
    Category.CACHES: Path.home() / "Library" / "Caches" / "com.apple.dt.Xcode",
}
