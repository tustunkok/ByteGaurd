# ByteGaurd (Yes, it is not a typo)

This Python script monitors **disk read activity** for a specified process and its child processes. If no significant disk read activity is detected for a certain period, the script will shut down the computer (or simulate shutdown in dry run mode).

## Features

- **Monitors disk read activity** for a specified process and its dynamic children.
- **Automatically shuts down the computer** if no significant disk read activity is detected for a specified amount of time.
- **Ignores small increases in disk read activity** below a configurable threshold.
- Allows customization of the target process name, idle time limit, byte threshold, and check interval through command-line arguments.
- Includes a dry run mode to simulate the shutdown process without actually shutting down.

## Requirements

- Python 3.x
- `psutil` library (`pip install psutil`)

## Usage

To run the script, execute the following command in your terminal:

```bash
python main.py --process-name chrome.exe --idle-time-limit 60 --byte-threshold 1024 --check-interval 5 --dry-run
```

### Command-Line Arguments

- `--process-name`: The name of the process to monitor (default: `chrome.exe`).
- `--process-id`: The process ID to monitor (default: `0`, meaning process name will be used).
- `--idle-time-limit`: The time limit in seconds for which no significant disk read activity is allowed before shutting down (default: `30`).
- `--byte-threshold`: The threshold in bytes for disk read activity changes that should be considered significant (default: `1024`).
- `--check-interval`: The interval in seconds between checks for disk read activity (default: `2`).
- `--dry-run`: If set, the script will simulate shutdown without actually shutting down.

### Example

To monitor disk read activity for Firefox, with a 120-second idle time limit, a byte threshold of 2048 bytes, and checking every 10 seconds, run:

```bash
python main.py --process-name firefox.exe --idle-time-limit 120 --byte-threshold 2048 --check-interval 10 --dry-run
```

### Dry Run Mode

To test the script without actually shutting down your computer, add the `--dry-run` flag:

```bash
python main.py --process-name chrome.exe --idle-time-limit 60 --byte-threshold 1024 --check-interval 5 --dry-run
```

This will print out what actions would be taken if the conditions were met, without performing them.

## Important Notes

- **This script monitors disk read activity, not network activity.** If you want to monitor network usage, this script will not work for that purpose.
- The script tracks the specified process and all its child processes dynamically.
- For processes that do not perform significant disk reads (such as some server applications), this script may not detect activity