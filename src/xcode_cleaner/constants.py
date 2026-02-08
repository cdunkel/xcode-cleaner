from __future__ import annotations

from enum import Enum
from pathlib import Path


class Category(Enum):
    DERIVED_DATA = "Derived Data"
    ARCHIVES = "Archives"
    IOS_DEVICE_SUPPORT = "iOS Device Support"
    WATCHOS_DEVICE_SUPPORT = "watchOS Device Support"
    TVOS_DEVICE_SUPPORT = "tvOS Device Support"
    SIMULATORS = "Simulators"
    CACHES = "Xcode Caches"


XCODE_BASE = Path.home() / "Library" / "Developer" / "Xcode"

CATEGORY_PATHS: dict[Category, Path] = {
    Category.DERIVED_DATA: XCODE_BASE / "DerivedData",
    Category.ARCHIVES: XCODE_BASE / "Archives",
    Category.IOS_DEVICE_SUPPORT: XCODE_BASE / "iOS DeviceSupport",
    Category.WATCHOS_DEVICE_SUPPORT: XCODE_BASE / "watchOS DeviceSupport",
    Category.TVOS_DEVICE_SUPPORT: XCODE_BASE / "tvOS DeviceSupport",
    Category.CACHES: Path.home() / "Library" / "Caches" / "com.apple.dt.Xcode",
}
