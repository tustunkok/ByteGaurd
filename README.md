# Download Activity Monitor

This Python script monitors download activity for a specified process and shuts down the computer if no significant activity is detected for a certain period of time.

## Features

- **Monitors download activity** for a specified process.
- **Automatically shuts down the computer** if no significant activity is detected for a specified amount of time.
- **Ignores increases in download activity** smaller than a specified threshold.
- Allows customization of the target process name, idle time limit, byte threshold, and check interval through command-line arguments.
- Includes a dry run mode to simulate the shutdown process without actually shutting down.

## Requirements

- Python 3.x
- `psutil` library (can be installed using `pip install psutil`)
- Administrative privileges to execute the shutdown command

## Usage

To run the script, simply execute the following command in your terminal:

```bash
python main.py --process-name chrome.exe --idle-time-limit 60 --byte-threshold 1024 --check-interval 5 --dry-run False
```

### Command-Line Arguments

- `--process-name`: The name of the process to monitor (default: `chrome.exe`).
- `--idle-time-limit`: The time limit in seconds for which no significant activity is allowed before shutting down (default: `60`).
- `--byte-threshold`: The threshold in bytes for download activity changes that should be considered significant (default: `1024`).
- `--check-interval`: The interval in seconds between checks for download activity (default: `5`).
- `--dry-run`: A flag to indicate whether the script should simulate a shutdown without actually shutting down (default: `False`).

### Example

To monitor download activity for Firefox, ignoring idle time for 120 seconds, with a byte threshold of 2048 bytes and checking every 10 seconds, you would run:

```bash
python main.py --process-name firefox.exe --idle-time-limit 120 --byte-threshold 2048 --check-interval 10 --dry-run False
```

### Dry Run Mode

If you want to test the script without actually shutting down your computer, set `--dry-run True`:

```bash
python main.py --process-name chrome.exe --idle-time-limit 60 --byte-threshold 1024 --check-interval 5 --dry-run True
```

This will print out what actions would be taken if the conditions were met without actually performing them.
