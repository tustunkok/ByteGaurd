import psutil
import time
import os
import sys
import argparse

# ==== CONFIGURATION ====
PROCESS_NAME = "chrome.exe"   # Target process name
IDLE_TIME_LIMIT = 30          # Seconds of no significant activity before shutdown
BYTE_THRESHOLD = 1024         # Ignore increases smaller than this (1 KB)
CHECK_INTERVAL = 2            # Seconds between checks
# ========================

def find_process_by_name(name):
    """Find the first process matching the given name."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            return proc
    return None

def get_all_related_procs(main_proc):
    """Get the main process + all child processes recursively, fresh each time."""
    procs = []
    try:
        procs.append(main_proc)
        procs.extend(main_proc.children(recursive=True))
    except psutil.NoSuchProcess:
        pass
    return procs

def get_total_read_bytes(procs):
    """Sum read_bytes for a list of processes."""
    total = 0
    for p in procs:
        try:
            total += p.io_counters().read_bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return total

def main():
    parser = argparse.ArgumentParser(description="Monitor download activity and shut down if no significant activity.")
    parser.add_argument('--process-name', default=PROCESS_NAME, help='Target process name')
    parser.add_argument('--idle-time-limit', type=int, default=IDLE_TIME_LIMIT, help='Seconds of no significant activity before shutdown')
    parser.add_argument('--byte-threshold', type=int, default=BYTE_THRESHOLD, help='Ignore increases smaller than this (in bytes)')
    parser.add_argument('--check-interval', type=int, default=CHECK_INTERVAL, help='Seconds between checks')
    parser.add_argument('--dry-run', action='store_true', help='Simulate the shutdown process without actually shutting down')

    args = parser.parse_args()

    process_name = args.process_name
    idle_time_limit = args.idle_time_limit
    byte_threshold = args.byte_threshold
    check_interval = args.check_interval
    dry_run = args.dry_run

    proc = find_process_by_name(process_name)
    if not proc:
        print(f"Process {process_name} not found.")
        sys.exit(1)

    print(f"Monitoring {process_name} (PID: {proc.pid}) and all dynamic children for download activity...")

    # Initial byte count
    last_bytes = get_total_read_bytes(get_all_related_procs(proc))
    last_active = time.time()

    while True:
        try:
            # Refresh list of processes each loop (catches new children)
            all_procs = get_all_related_procs(proc)
            current_bytes = get_total_read_bytes(all_procs)
            diff = current_bytes - last_bytes
            last_bytes = current_bytes

            if diff >= byte_threshold:
                last_active = time.time()
                print(f"Downloading... +{diff} bytes (total: {current_bytes})")
            else:
                idle_time = time.time() - last_active
                print(f"Only {diff} bytes in last check — idle for {idle_time:.1f} seconds.")
                if idle_time >= idle_time_limit:
                    if dry_run:
                        print("Dry run: Shutdown would have been executed.")
                        break
                    else:
                        print("Download finished. Shutting down...")
                        os.system("shutdown /s /t 0")
                        break

            time.sleep(check_interval)

        except psutil.NoSuchProcess:
            print("Main process closed.")
            break

if __name__ == "__main__":
    main()