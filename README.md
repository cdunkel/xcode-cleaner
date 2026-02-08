# xcode-cleaner

A CLI tool to reclaim disk space from Xcode build artifacts, caches, and simulators.

## What It Scans

| Category | Path |
|----------|------|
| Derived Data | `~/Library/Developer/Xcode/DerivedData` |
| Archives | `~/Library/Developer/Xcode/Archives` |
| iOS Device Support | `~/Library/Developer/Xcode/iOS DeviceSupport` |
| watchOS Device Support | `~/Library/Developer/Xcode/watchOS DeviceSupport` |
| tvOS Device Support | `~/Library/Developer/Xcode/tvOS DeviceSupport` |
| Simulators | Managed via `xcrun simctl` |
| Xcode Caches | `~/Library/Caches/com.apple.dt.Xcode` |

## Installation

From PyPI:

```
pip install xcode-cleaner
```

From source:

```
git clone https://github.com/cdunkel/xcode-cleaner.git
cd xcode-cleaner
pip install .
```

## Usage

**Scan and display a disk usage report:**

```
xcode-cleaner scan
```

**Interactively select and delete items to free space:**

```
xcode-cleaner clean
```

**Preview what would be deleted without actually deleting:**

```
xcode-cleaner clean --dry-run
```

## Requirements

- macOS
- Python 3.9+
- Xcode (for simulator management)

## License

MIT
