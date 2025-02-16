# Windows Time Sync Tray App

A simple system tray application that automatically synchronizes Windows time. Features include:
- Manual time synchronization
- Automatic synchronization every minute
- System tray interface with start/stop functionality
- System tray notifications for sync status

## Requirements
- Python 3.6+
- PyQt5
- Windows OS (uses w32tm)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pimpmuckl/windows-time-sync-tray
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run directly with Python (requires administrator privileges):
```bash
python time_sync.py
```

Or build executable:
```bash
python -m PyInstaller --windowed --onefile --icon=clock.ico time_sync.py
```

## License

MIT License - See LICENSE file for details
